output "eks_cluster_name" {
  value = aws_eks_cluster.mlops_cluster.name
}

output "eks_cluster_endpoint" {
  value = aws_eks_cluster.mlops_cluster.endpoint
}
