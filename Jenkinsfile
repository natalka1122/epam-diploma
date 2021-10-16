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
        input 'docker-compose down'
      }
    }
    stage('docker up') {
      steps {
        input 'docker-compose up -d'
      }
    }
  }
}
