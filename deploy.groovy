def kubectl(namespace, command) {
    container('kubectl') {
        sh("kubectl --namespace=${namespace} ${command}")
    }
}

def toKubernetes(tagToDeploy, namespace, deploymentName) {
    sh("sed -i.bak 's#BUILD_TAG#${tagToDeploy}#' ./chapter-10/deploy/${namespace}/*.yml")

    kubectl(namespace, "apply -f chapter-10/deploy/${namespace}/")
}

def rollback(deploymentName) {
    kubectl("rollout undo deployment/${deploymentName}")
}

return this;