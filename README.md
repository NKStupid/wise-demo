# wise-demo

# 727922501631
# arn:aws:iam::727922501631:role/iam-rol-ecs-wise-dev


docker run -e KEYCLOAK_USER=admin -e KEYCLOAK_PASSWORD=admin -p 8080:8080 quay.io/keycloak/keycloak

docker run -e KEYCLOAK_USER=admin -e KEYCLOAK_PASSWORD=admin -p 8443:8443 quay.io/keycloak/keycloak

