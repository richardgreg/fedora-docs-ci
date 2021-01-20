openshift.withCluster() {
  env.NAMESPACE = openshift.project()
  env.BUILD_SCRIPT = env.BUILD_CONTEXT_DIR ? "${env.BUILD_CONTEXT_DIR}/build.sh" : "build.sh"
  echo "Starting Pipeline for ${env.APP_NAME}..."
  env.BUILD = "${env.NAMESPACE_BUILD}"
  env.STAGE = "${env.NAMESPACE_STAGE}"
  env.PROD = "${env.NAMESPACE_PROD}"
}

pipeline {
  // Use Jenkins Maven slave
  // Jenkins will dynamically provision this as OpenShift Pod
  // All the stages and steps of this Pipeline will be executed on this Pod
  // After Pipeline completes the Pod is killed so every run will have clean
  // workspace
  agent {
    label 'maven'
  }

  // Pipeline Stages start here
  // Requires at least one stage
  stages {

    // Checkout source code
    // This is required as Pipeline code is originally checkedout to
    // Jenkins Master but this will also pull this same code to this slave
    stage('Git Checkout') {
      steps {
        // Turn off Git's SSL cert check, uncomment if needed
        sh 'git config --global http.sslVerify false'
        git url: "${APPLICATION_SOURCE_REPO}", branch: "${APPLICATION_SOURCE_REF}"
      }
    }

    // Run Maven build, skipping tests
    stage('Build'){
      steps {

        sh """
        sudo dnf install podman
        ./${BUILD_SCRIPT}
        """
      }
    }
  }
}
