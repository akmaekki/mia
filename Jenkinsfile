def withPod(body) {
  podTemplate(label: 'pod', serviceAccount: 'jenkins', containers: [
      containerTemplate(name: 'docker', image: 'docker', command: 'cat', ttyEnabled: true),
      containerTemplate(name: 'kubectl', image: 'lachlanevenson/k8s-kubectl', command: 'cat', ttyEnabled: true)
    ],
    volumes: [
      hostPathVolume(mountPath: '/var/run/docker.sock', hostPath: '/var/run/docker.sock'),
    ]
 ) { body() }
}

withPod {
  node('pod') {
    def tag = "${env.BRANCH_NAME}.${env.BUILD_NUMBER}"
    def service = "market-data:${tag}"

    checkout scm

    container('docker') {
      stage('Build') {
        sh("docker build -f ./chapter-10/market-data/Dockerfile -t ${service} ./chapter-10/market-data")
      }

      stage('Test') {
        try {
          sh("docker run -v `pwd`:/workspace --rm ${service} python setup.py test")
          sh("echo Host `hostname`")
          sh("echo PWD `pwd`")
        } finally {
          step([$class: 'JUnitResultArchiver', testResults: '**/results.xml'])
        }
      }

      def tagToDeploy = "akmaekki/${service}"
      stage('Publish') {
        withDockerRegistry(registry: [credentialsId: 'dockerhub']) {
          sh("docker tag ${service} ${tagToDeploy}")
          sh("docker push ${tagToDeploy}")
        }
      }

      def deploy = load 'deploy.groovy'
      stage('Deploy to staging') {
        deploy.toKubernetes(tagToDeploy, 'staging', 'market-data')
      }

      stage('Deploy canary') {
        deploy.toKubernetes(tagToDeploy, 'canary', 'market-data-canary')

        try {
          input message: "Continue releasing ${tagToDeploy} to production?"
        } catch (Exception e) {
          deploy.rollback('market-data-canary') #B
        }
      }

      stage('Deploy to production') {
        deploy.toKubernetes(tagToDeploy, 'production', 'market-data')
      }
    }
  }
}