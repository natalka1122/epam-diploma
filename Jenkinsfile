import groovy.transform.Field
@Field def image_names
@Field def image_build
@Field def registry_credential_set

pipeline {
  agent any
  environment {
    TOKEN = credentials('botSecret')
    CHAT_ID = credentials('chatId')
  }
  stages {
    stage('init vars') {
      steps{
        script {
          image_names = ['frontend', 'backend']
          image_build = []
          registry_credential_set = 'dockerhub'
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
        script {
          withCredentials([usernamePassword(credentialsId: registry_credential_set, passwordVariable: 'password', usernameVariable: 'username')]) {
            for (int i = 0; i < image_names.size(); i++) {
              image_build.add(docker.build("${username}/${image_names[i]}","--build-arg SOURCE_DIR=${image_names[i]}/ ."))
            }
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
        script {
          for (int i = 0; i < image_build.size(); i++) {
            image_build[i].inside('-u root'){
              sh 'apk add --update gcc libc-dev'
              sh 'pip install --upgrade pylint black'
              sh 'cd /app && python3 -m pylint *.py --output-format=parseable --fail-under=9 --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}"| tee pylint.log'
              sh 'cd /app && python3 -m black *.py --diff'
              sh 'cd /app && python3 -m black *.py --check'
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
          docker.withRegistry('', registry_credential_set) {
            for (int i = 0; i < image_build.size(); i++) {
              image_build[i].push()
            }
          }
        }
      }
    }
    stage('dev environment') {
      agent {
        node {
          label 'proxmox'
        }
      }
      steps {
        sh 'docker-compose down'
        sh 'docker-compose up -d'
      }
    }
    stage('Ready for prod?') {
      steps {
        input message: "Are we ready for prod?"
      }
    }
    stage('Deploy to prod') {
      steps {
        echo "Kubernetes"
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
