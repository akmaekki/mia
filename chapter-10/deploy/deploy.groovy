def toKubernetes(tagToDeploy, namespace) {
    sh("sed -i.bak 's#BUILD_TAG#${tagToDeploy}#' ./chapter-10/deploy/${namespace}/*.yml")

    kubectl("apply -f chapter-10/deploy/${namespace}/")
}

def kubectl(namespace, command) {
    container('kubectl') {
        sh("kubectl --namespace=${namespace} ${command}")
    }
}

def rollback(deploymentName) {
    kubectl("rollout undo deployment/${deploymentName}")
}

return this;
