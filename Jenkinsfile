pipeline {
  agent any
  environment {
    TOKEN = credentials('botSecret')
    CHAT_ID = credentials('chatId')
    image_name_frontend = 'natalka1122/epam-diploma-frontend'
    registryCredentialSet = 'dockerhub'
  }
  stages {
    def image_names = ['frontend', 'backend']
    def image_build = []
    stage('build frontend'){
      agent {
        node {
          label 'proxmox'
        }
      }
      steps {
        echo 'Building container image...'
        script {
          for (int i = 0; i < image_names.size(); i++) {
            echo "image_name = ${image_names[i]}"
            image_build.add(docker.build("${image_names[i]}","--build-arg SOURCE_DIR=${image_names[i]}/ ."))
          }
        }
      }
    }
    stage('Test') {
      agent {
        node {
          label 'proxmox'
        }
      }
      steps {
        echo 'Running tests inside the container...'
        script {
          for (int i = 0; i < image_build.size(); i++) {
            echo "image_build = ${image_build[i]}"
            image_build[i].inside('-u root'){
              sh 'pip install -r /app/requirements.txt'
              sh 'pip install --upgrade pylint'
              sh 'cd /app && python3 -m pylint --output-format=parseable --fail-under=9 --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" *.py | tee pylint.log || echo "pylint exited with $?"'
              sh 'sleep 1000'
            }
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
