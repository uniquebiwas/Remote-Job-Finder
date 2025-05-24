pipeline {
  agent any

  environment {
    HARBOR_URL     = "harbor.biwaspudasaini.info.np"
    HARBOR_PROJECT = "myproject"
    IMAGE_NAME     = ""
    IS_TAG         = "false"
    GIT_TAG        = ""
  }

  stages {
    stage('Clone Repo') {
      steps {
        script {
          git url: 'https://github.com/uniquebiwas/Remote-Job-Finder.git'

          // Get image name from repo
          env.IMAGE_NAME = env.GIT_URL.tokenize('/').last().replace('.git','')

          // Fetch tags
          sh "git fetch --tags"

          // Check if this is a tag push
          env.IS_TAG = sh(script: "git describe --tags --exact-match > /dev/null 2>&1 && echo true || echo false", returnStdout: true).trim()
        }
      }
    }

    stage('Validate Tag') {
      when {
        expression { env.IS_TAG == 'true' }
      }
      steps {
        script {
          env.GIT_TAG = sh(script: "git describe --tags --exact-match", returnStdout: true).trim()
          echo "Detected tag: ${env.GIT_TAG}"
        }
      }
    }

    stage('Build and Push Docker Image') {
      when {
        expression { env.IS_TAG == 'true' }
      }
      steps {
        withCredentials([usernamePassword(credentialsId: 'harbor-creds', usernameVariable: 'HARBOR_USER', passwordVariable: 'HARBOR_PASS')]) {
          script {
            def imageTag = "${env.HARBOR_URL}/${env.HARBOR_PROJECT}/${env.IMAGE_NAME}:${env.GIT_TAG}"
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
      when {
        expression { env.IS_TAG == 'true' }
      }
      steps {
        echo "Hello 👋 - Image pushed for tag: ${env.GIT_TAG}"
      }
    }

    stage('Cleanup Workspace') {
      steps {
        cleanWs()
      }
    }
  }
}
