resource "aws_eks_cluster" "mlops_cluster" {
  name     = var.cluster_name
  role_arn = "arn:aws:iam::123456789012:role/EKSClusterRole"

  vpc_config {
    subnet_ids = ["subnet-xxxxxx", "subnet-yyyyyy"]
  }
}
