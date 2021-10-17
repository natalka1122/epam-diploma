pipeline {
  agent any
  environment {
    TOKEN = credentials('botSecret')
    CHAT_ID = credentials('chatId')
  }
  stages {
    stage('lint') {
      agent {
        node {
          label 'java-docker-slave'
        }
      }
      steps {
        sh 'echo 1'
        sh 'python3 -m pylint --output-format=parseable --fail-under=9 frontend --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" | tee pylint.log || echo "pylint exited with $?"'
        sh 'python3 -m pylint --output-format=parseable --fail-under=9 backend --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" | tee pylint.log || echo "pylint exited with $?"'
        input "2"
      }
    }
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
