pipeline {
  agent any

  environment {
    HARBOR_URL     = "harbor.biwaspudasaini.info.np"
    HARBOR_PROJECT = "myproject"
    IMAGE_NAME     = ""
    IMAGE_TAG      = ""  // You can default this to a branch name or timestamp
  }

  stages {
    stage('Clone Repo') {
      steps {
        script {
          git url: 'https://github.com/uniquebiwas/Remote-Job-Finder.git'

          // Get image name from repo
          env.IMAGE_NAME = env.GIT_URL.tokenize('/').last().replace('.git','')

          // Set tag to short commit hash or branch name
          env.IMAGE_TAG = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
        }
      }
    }

    stage('Build and Push Docker Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'harbor-creds', usernameVariable: 'HARBOR_USER', passwordVariable: 'HARBOR_PASS')]) {
          script {
            def imageTag = "${env.HARBOR_URL}/${env.HARBOR_PROJECT}/${env.IMAGE_NAME}:${env.IMAGE_TAG}"
            sh """
              docker build -t ${imageTag} .
              echo "Logging into Harbor"
              docker login ${env.HARBOR_URL} -u ${HARBOR_USER} -p ${HARBOR_PASS}
              docker push ${imageTag}
              docker rmi ${imageTag}
            """
          }
        }
      }
    }

    stage('Say Hello') {
      steps {
        echo "Hello 👋 - Image pushed for commit/tag: ${env.IMAGE_TAG}"
      }
    }

    stage('Cleanup Workspace') {
      steps {
        cleanWs()
      }
    }
  }
}
