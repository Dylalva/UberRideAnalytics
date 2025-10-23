provider "aws" {
  region = "us-east-2"
}

resource "aws_key_pair" "deployer" {
  key_name   = "deployer1"
  public_key = file("~/.ssh/id_rsa_flaskapp.pub")
}

resource "aws_security_group" "web_sg" {
  name        = "flask-teensmart-sg"
  description = "SSH, HTTP, HTTPS y Docker"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "SSH"
  }
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTP"
  }
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS"
  }
  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Docker App"
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "web" {
  ami                    = "ami-0d1b5a8c13042c939" # Ubuntu 22.04 LTS
  instance_type          = "t2.micro"
  key_name               = aws_key_pair.deployer.key_name
  vpc_security_group_ids = [aws_security_group.web_sg.id]
}

output "public_ip" {
  value = aws_instance.web.public_ip
  description = "La dirección IP pública de la instancia EC2"
}

output "ssh_connection" {
  value = "ssh -i ~/.ssh/id_rsa_flaskapp ubuntu@${aws_instance.web.public_ip}"
  description = "Comando para conectarse por SSH a la instancia"
}