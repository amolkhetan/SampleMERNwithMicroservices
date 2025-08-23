pipeline {
  agent any

  environment {
    AWS_REGION = 'us-west-2'
    ECR_REGISTRY = '975050024946.dkr.ecr.us-west-2.amazonaws.com'
    IMAGE_TAG = "1.0"
  }

  stages {
    stage('Checkout') {
      steps {
        git branch: 'main',
            credentialsId: 'github-creds',
            url: 'https://github.com/amolkhetan/SampleMERNwithMicroservices'
      }
    }

    stage('Login to ECR') {
      steps {
        sh '''
          aws ecr get-login-password --region $AWS_REGION | \
          docker login --username AWS --password-stdin $ECR_REGISTRY
        '''
      }
    }

    stage('Build & Push hello') {
      steps {
        script {
          def rawName = 'helloService'
          def imageName = rawName.toLowerCase()
          docker.build("${imageName}:${IMAGE_TAG}", "./backend/${rawName}")
          sh """
            docker tag ${imageName}:${IMAGE_TAG} $ECR_REGISTRY/${imageName}:${IMAGE_TAG}
            docker push $ECR_REGISTRY/${imageName}:${IMAGE_TAG}
          """
        }
      }
    }

    stage('Build & Push profile') {
      steps {
        script {
          def rawName = 'profileService'
          def imageName = rawName.toLowerCase()
          docker.build("${imageName}:${IMAGE_TAG}", "./backend/${rawName}")
          sh """
            docker tag ${imageName}:${IMAGE_TAG} $ECR_REGISTRY/${imageName}:${IMAGE_TAG}
            docker push $ECR_REGISTRY/${imageName}:${IMAGE_TAG}
          """
        }
      }
    }

    stage('Build & Push frontend') {
      steps {
        script {
          def rawName = 'frontend'
          def imageName = rawName.toLowerCase()
          docker.build("${imageName}:${IMAGE_TAG}", "./${rawName}")
          sh """
            docker tag ${imageName}:${IMAGE_TAG} $ECR_REGISTRY/${imageName}:${IMAGE_TAG}
            docker push $ECR_REGISTRY/${imageName}:${IMAGE_TAG}
          """
        }
      }
    }
  }
}
