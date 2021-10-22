pipeline {
  agent any
  environment {
    TOKEN = credentials('botSecret')
    CHAT_ID = credentials('chatId')
    image_name_frontend = "natalka1122/epam-diploma-frontend"
    registryCredentialSet = 'dockerhub'
  }
  stages {
    stage('build frontend'){
      agent {
        node {
          label 'proxmox'
        }
      }
      steps {
        echo 'Building container image...'
        script {
          dockerInstance = docker.build("frontend","--build-arg SOURCE_DIR=frontend/ .")
        }
      }
    }
    stage('Test') {
      steps {
        echo 'Running tests inside the container...'
        script {
          dockerInstance.inside('-u root'){
            sh 'pip install -r frontend/requirements.txt'
            sh 'pip install --upgrade pylint'
            sh 'python3 -m pylint --output-format=parseable --fail-under=9 frontend --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" | tee pylint.log || echo "pylint exited with $?"'
            sh 'sleep 1000'
          }
        }
      }
    }
    // stage('lint') {
    //   agent {
    //     node {
    //       label 'java-docker-slave'
    //     }
    //   }
    //   steps {
    //     input "1"
    //     sh 'python -m venv venv && source venv/bin/activate && pip install -r frontend/requirements.txt'
    //     sh 'python3 -m pylint --output-format=parseable --fail-under=9 frontend --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" | tee pylint.log || echo "pylint exited with $?"'
    //     sh 'python3 -m pylint --output-format=parseable --fail-under=9 backend --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" | tee pylint.log || echo "pylint exited with $?"'
    //     input "2"
    //   }
    // }
    stage('docker-compose full restart') {
      agent {
        node {
          label 'proxmox'
        }
      }
      steps {
        sh 'docker-compose down'
        sh 'docker-compose build'
        sh 'docker-compose up -d'
      }
    }
  }
  post {
    success {
      node('java-docker-slave') {
        sh 'wget -qO- --post-data="parse_mode=markdown&chat_id=' + CHAT_ID + '&text=*' + env.JOB_NAME+ '* : POC *Branch*: ' + env.GIT_BRANCH + ' *Build* : OK *Published* = YES" https://api.telegram.org/bot' + TOKEN + '/sendMessage'
      }
    }

    aborted {
      node('java-docker-slave') {
        sh 'wget -qO- --post-data="parse_mode=markdown&chat_id=' + CHAT_ID + '&text=*' + env.JOB_NAME+ '* : POC *Branch*: ' + env.GIT_BRANCH + ' *Build* : Aborted *Published* = Aborted" https://api.telegram.org/bot' + TOKEN + '/sendMessage'
      }
    }

    failure {
      node('java-docker-slave') {
        sh 'wget -qO- --post-data="parse_mode=markdown&chat_id=' + CHAT_ID + '&text=*' + env.JOB_NAME+ '* : POC *Branch*: ' + env.GIT_BRANCH + ' *Build* : not OK *Published* = NO" https://api.telegram.org/bot' + TOKEN + '/sendMessage'
      }
    }
  }
}
