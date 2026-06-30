# DB SUBNET GROUP (PRIVATE SUBNETS)

resource "aws_db_subnet_group" "mysql" {
  name       = "${var.project_name}-mysql-subnet"
  subnet_ids = module.vpc.private_subnets

  tags = {
    Name = "${var.project_name}-mysql-subnet"
  }
}

# RDS SECURITY GROUP

resource "aws_security_group" "rds" {
  name   = "${var.project_name}-rds-sg"
  vpc_id = module.vpc.vpc_id

  tags = {
    Name = "${var.project_name}-rds-sg"
  }
}

# INGRESS RULE (ALLOW EKS VPC ACCESS)

resource "aws_vpc_security_group_ingress_rule" "mysql" {

  security_group_id = aws_security_group.rds.id

  ip_protocol = "tcp"
  from_port   = 3306
  to_port     = 3306

  # Allow only internal VPC traffic (EKS → RDS)
  cidr_ipv4 = module.vpc.vpc_cidr_block
}

# RDS MYSQL CREATION

resource "aws_db_instance" "mysql" {

  identifier = "${var.project_name}-mysql"

  engine         = "mysql"
  engine_version = "8.0"

  instance_class = "db.t3.micro"

  allocated_storage = 20

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  db_subnet_group_name   = aws_db_subnet_group.mysql.name
  vpc_security_group_ids = [aws_security_group.rds.id]

  skip_final_snapshot = true

  # PRIVATE DATABASE 

  publicly_accessible = false

  tags = {
    Name = "${var.project_name}-mysql"
  }
  lifecycle {
    ignore_changes = all
  }
}