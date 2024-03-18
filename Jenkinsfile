pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',  url: 'https://github.com/uniquebiwas/Remote-Job-Finder'
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

        stage('Stop and Remove Container') {
            steps {
                script {
                    // Stop and remove the existing container if it exists
                    sh 'docker-compose down || true'
                    sh 'pip install --upgrade pip'
                }
            }
        }

        stage('Build and Run') {
            steps {
                script {
                    // Build the Docker image and run the container
                    sh 'docker build -t remotejobimage:latest -f Dockerfile .'


                }
            }
        }
        stage('Login to Docker Hub and Push to docker hub') {
            steps {
                script {
                    
                    withCredentials([usernamePassword(credentialsId:"dockerHub",passwordVariable:"dockerpass",usernameVariable:"user")]){
                    sh "docker tag remotejobimage:latest ${env.user}/remotejobimage:latest"
                    sh "echo ${env.dockerpass} | docker login -u ${env.user} --password-stdin"
                    sh "docker push ${env.user}/remotejobimage:latest"

                    }
        
                }
            }
        }
    }
}
