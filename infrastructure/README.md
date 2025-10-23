<details>
<summary><h2>English</h2></summary>

# TeenSmartInsight Deployment with Terraform

This directory contains the Terraform configuration to deploy the TeenSmartInsight application on AWS.

## Prerequisites

1. Terraform [installed](https://www.terraform.io/downloads.html)  
2. An AWS account with credentials configured

## AWS Credentials Configuration

Before running Terraform, you need to configure your AWS credentials. You have several options:

### Option 1: AWS credentials file

Create or edit the file `~/.aws/credentials`:

```ini
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

### Option 2: Environment variables

Set the following environment variables in your shell:

```bash
export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY"
export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_KEY"
```

### Option 3: Hardcode credentials in `main.tf` (not recommended)

Uncomment and edit the `access_key` and `secret_key` lines in your `main.tf` (avoid committing this to public repositories).

## Deployment

1. Initialize Terraform:

   ```bash
   terraform init
   ```

2. Review the execution plan:

   ```bash
   terraform plan
   ```

3. Apply the configuration:

   ```bash
   terraform apply
   ```

4. Type `yes` to confirm when prompted.

After the deployment completes, Terraform will output the instance’s public IP and the SSH connection command.

## Deployment Instructions

### Prerequisites

1. Generate SSH Key for Deployment

   ```bash
   # Generate a new SSH key pair
   ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa_flaskapp -C "your_email@example.com"
   
   # Set proper permissions
   chmod 600 ~/.ssh/id_rsa_flaskapp
   ```

2. Update the `hosts.ini` file in the `infrastructure` directory with your server's IP address:

   ```ini
   [web]
   YOUR_SERVER_IP
   
   [web:vars]
   ansible_user=ubuntu
   ansible_ssh_private_key_file=~/.ssh/id_rsa_flaskapp
   ansible_ssh_common_args='-o StrictHostKeyChecking=no'
   ```

3. Deploy with Docker using Ansible:

   ```bash
   cd infrastructure
   ansible-playbook deploy-with-docker.yml -i hosts.ini
   ```

   This will deploy the application using Docker on your server with HTTPS configuration.


## Destroying the Infrastructure

To tear down all resources created by this configuration:

```bash
terraform destroy
```

</details>

<details>
<summary><h2>Español</h2></summary>

# Despliegue de TeenSmartInsight con Terraform

Este directorio contiene la configuración de Terraform para desplegar la aplicación TeenSmartInsight en AWS.

## Requisitos previos

1. Tener instalado [Terraform](https://www.terraform.io/downloads.html)
2. Tener una cuenta de AWS y credenciales configuradas

## Configuración de credenciales AWS

Antes de ejecutar Terraform, necesitas configurar tus credenciales de AWS. Tienes varias opciones:

### Opción 1: Archivo de credenciales AWS

Crea o edita el archivo `~/.aws/credentials`:

```
[default]
aws_access_key_id = TU_ACCESS_KEY
aws_secret_access_key = TU_SECRET_KEY
```

### Opción 2: Variables de entorno

Configura las siguientes variables de entorno:

```bash
export AWS_ACCESS_KEY_ID="TU_ACCESS_KEY"
export AWS_SECRET_ACCESS_KEY="TU_SECRET_KEY"
```

### Opción 3: Credenciales en el archivo main.tf

Descomenta y edita las líneas de `access_key` y `secret_key` en el archivo `main.tf` (no recomendado para repositorios públicos).

## Despliegue

1. Inicializa Terraform:
   ```bash
   terraform init
   ```

2. Verifica el plan de ejecución:
   ```bash
   terraform plan
   ```

3. Aplica la configuración:
   ```bash
   terraform apply
   ```

4. Confirma la operación escribiendo `yes` cuando se te solicite.

## Acceso a la aplicación

Una vez completado el despliegue, Terraform mostrará la IP pública de la instancia y el comando para conectarse por SSH.

## Instrucciones de Despliegue de la aplicación

### Requisitos Previos

1. Generar Clave SSH para el Despliegue

   ```bash
   # Generar un nuevo par de claves SSH
   ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa_flaskapp
   
   # Establecer permisos adecuados
   chmod 600 ~/.ssh/id_rsa_flaskapp
   ```

2. Actualizar el archivo `hosts.ini` en el directorio `infrastructure` con la dirección IP de tu servidor:

   ```ini
   [web]
   TU_IP_DE_SERVIDOR
   
   [web:vars]
   ansible_user=ubuntu
   ansible_ssh_private_key_file=~/.ssh/id_rsa_flaskapp
   ansible_ssh_common_args='-o StrictHostKeyChecking=no'
   ```

3. Desplegar con Docker usando Ansible:

   ```bash
   cd infrastructure
   ansible-playbook deploy-with-docker.yml -i hosts.ini
   ```

   Esto desplegará la aplicación usando Docker en tu servidor con configuración HTTPS.


## Destruir la infraestructura

Para eliminar todos los recursos creados:

```bash
terraform destroy
```
</details>