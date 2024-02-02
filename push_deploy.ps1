docker login
docker buildx build --platform linux/amd64 -t uniquebiwas/testjob .
docker push uniquebiwas/testjob
