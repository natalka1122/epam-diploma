pipeline {
  agent {
    label 'proxmox'
  }
  stages {
    stage('docker build') {
      steps {
        sh 'docker-compose build'
      }
    }
    stage('docker down') {
      steps {
        sh 'docker-compose down'
      }
    }
    stage('docker up') {
      steps {
        sh 'docker-compose up -d'
      }
    }
  }
  post {
    success {
      telegramSend 'success'
    }
    aborted {
      telegramSend 'aborted'
    }
    failure {
      telegramSend 'failure'
    }
  }
}
