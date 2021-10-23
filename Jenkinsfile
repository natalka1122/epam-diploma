import groovy.transform.Field
@Field def image_names
@Field def image_build

pipeline {
  agent any
  environment {
    TOKEN = credentials('botSecret')
    CHAT_ID = credentials('chatId')
    image_name_frontend = 'natalka1122/epam-diploma-frontend'
    registryCredentialSet = 'dockerhub'
  }
  stages {
    stage('init vars') {
      steps{
        script {
          image_names = ['frontend', 'backend']
          image_build = []
        }
      }
    }
    stage('build'){
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
              sh 'sleep 1'
            }
          }
        }
      }
    }
    stage('push images') {
      agent {
        node {
          label 'proxmox'
        }
      }
      steps {
        script {
          docker.withRegistry('', registryCredentialSet) {
            for (int i = 0; i < image_build.size(); i++) {
              echo "image_build = ${image_build[i]}"
              image_build[i].push()
          }
        }
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
