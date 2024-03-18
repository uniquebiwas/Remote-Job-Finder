pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/uniquebiwas/Remote-Job-Finder'
            }
        }

        stage('Cleanup') {
            steps {
                script {
                    // Remove unused Docker images and containers
                    sh 'docker image prune -f'
                    sh 'docker container prune -f'
                }
            }
        }

        stage('Build and Run') {
            steps {
                script {
                    def tag = env.BRANCH_NAME.replaceAll("refs/tags/", "")
                    echo "Tag Name: $tag"
                    // Build the Docker image
                    sh 'docker build -t uniquebiwas/remotejobimage:latest .'
                }
            }
        }

        stage('Login to Docker Hub and Push to Docker Hub') {
            steps {
                script {
                    // Tag the Docker image with the latest tag
                    sh 'docker tag uniquebiwas/remotejobimage:latest uniquebiwas/remotejobimage:$tag'

                    // Login to Docker Hub and push the Docker image
                    withCredentials([usernamePassword(credentialsId: "dockerHub", passwordVariable: "dockerpass", usernameVariable: "user")]) {
                        sh "echo ${env.dockerpass} | docker login -u ${env.user} --password-stdin"
                        sh "docker push uniquebiwas/remotejobimage:$tag"
                    }
                }
            }
        }
    }
}
