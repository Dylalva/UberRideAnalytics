import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import make_column_selector as selector

# 1️⃣ Clase TimeFeatures
class TimeFeatures(BaseEstimator, TransformerMixin):
    """Agrega variables temporales derivadas de date y time."""
    def __init__(self, date_col="date", time_col="time", drop_original=True):
        self.date_col = date_col
        self.time_col = time_col
        self.drop_original = drop_original
        self._added = []

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        # date features
        if self.date_col in X:
            X["year"] = X[self.date_col].dt.year
            X["month"] = X[self.date_col].dt.month
            X["day_of_week"] = X[self.date_col].dt.dayofweek  # 0=Mon
            X["is_weekend"] = X["day_of_week"].isin([5,6]).astype(int)
            self._added += ["year","month","day_of_week","is_weekend"]
        # time features
        if self.time_col in X:
            X["hour"] = X[self.time_col].dt.hour
            bins = [-1,5,9,16,20,24]
            labels = ["late_night","morning_rush","daytime","evening","night"]
            X["hour_bin"] = pd.cut(X["hour"], bins=bins, labels=labels)
            self._added += ["hour","hour_bin"]

        if self.drop_original:
            X = X.drop(columns=[c for c in [self.date_col, self.time_col] if c in X], errors="ignore")
        return X

# 2️⃣ Clase RareCategoryGrouper
class RareCategoryGrouper(BaseEstimator, TransformerMixin):
    """Agrupa categorías raras como 'Other' en columnas categóricas."""
    def __init__(self, min_freq=0.01, columns=None, other_label="Other"):
        self.min_freq = min_freq
        self.columns = columns
        self.other_label = other_label
        self.keep_maps_ = {}

    def fit(self, X, y=None):
        X = X.copy()
        if self.columns is None:
            self.columns = X.select_dtypes(include="object").columns.tolist()
        for c in self.columns:
            vc = X[c].value_counts(normalize=True, dropna=False)
            keep = set(vc[vc >= self.min_freq].index)
            self.keep_maps_[c] = keep
        return self

    def transform(self, X):
        X = X.copy()
        for c in self.columns:
            if c in X:
                keep = self.keep_maps_[c]
                X[c] = X[c].where(X[c].isin(keep), other=self.other_label)
        return X

class RidePreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self, date_col="date", time_col="time", min_cat_freq=0.01):
        self.date_col = date_col
        self.time_col = time_col
        self.min_cat_freq = min_cat_freq
        self.time_features = TimeFeatures(date_col=date_col, time_col=time_col, drop_original=True)
        self.rare = RareCategoryGrouper(min_freq=min_cat_freq)
        self.column_transformer = None
        self.num_features_ = None
        self.cat_features_ = None

    def _remove_low_variance(self, X):
        """Elimina columnas numéricas sin varianza."""
        num = X.select_dtypes(include=np.number)
        keep = [c for c in num.columns if num[c].nunique() > 1]
        drop = [c for c in num.columns if num[c].nunique() <= 1]
        if drop:
            print(f"Eliminadas columnas sin varianza: {drop}")
        return X[keep + X.select_dtypes(exclude=np.number).columns.tolist()]

    def fit(self, X, y=None):
        X = X.copy()
        X = self.time_features.fit_transform(X)
        X = self.rare.fit_transform(X)
        X = self._remove_low_variance(X)

        self.num_features_ = selector(dtype_include=np.number)(X)
        self.cat_features_ = selector(dtype_include=object)(X)

        numeric_pipeline = Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler(with_mean=False))
        ])
        categorical_pipeline = Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse=True))
        ])

        self.column_transformer = ColumnTransformer([
            ("num", numeric_pipeline, self.num_features_),
            ("cat", categorical_pipeline, self.cat_features_)
        ], sparse_threshold=0.3)

        self.column_transformer.fit(X, y)
        return self

    def transform(self, X):
        X = X.copy()
        X = self.time_features.transform(X)
        X = self.rare.transform(X)

        # IMPORTANT: do not remove low-variance columns at transform time.
        # ColumnTransformer was fitted with a fixed set of columns in `fit`.
        # Dropping columns here can produce a columns-mismatch error.
        return self.column_transformer.transform(X)

    def get_feature_names(self):
        num_names = list(self.num_features_)
        cat_ohe = self.column_transformer.named_transformers_["cat"]["onehot"]
        cat_names = cat_ohe.get_feature_names_out(self.cat_features_).tolist()
        return num_names + cat_names