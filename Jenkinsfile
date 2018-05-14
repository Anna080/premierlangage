pipeline {
  agent any
  stages {
    stage('Configurations') {
      steps {
        sh '''  
               pwd
               source /srv/env/jenkinsenv/bin/activate
               cd server/serverpl
               echo "Environnement configuration..."
               ./install_local.sh
           '''
      }
    }
    stage('Test') {
      steps {
        sh '''
              cd server/serverpl
               echo "Running the tests..."
               python3 manage.py test
           '''
      }
    }
    stage('Clean') {
      steps {
        sh '''
           '''
      }
    }
  }
}
