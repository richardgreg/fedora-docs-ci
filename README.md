# CI/CD for Fedora Docs
Instructions on enabling continuous integration and development for the Fedora documentation website.

### 1. Create Lifecycle Stages
There are three stages for the application to be promoted through:

* fedora-documentation-build
* fedora-documentation-stage
* fedora-documentation-prod

Use the YAML that defines project requests to quickly create application
```
$ oc create -f .openshift/projects/projects.yml
project.project.openshift.io/fedora-documentation-build created
project.project.openshift.io/fedora-documentation-stage created
project.project.openshift.io/fedora-documentation-prod created
```

### 2. Start up Jenkins master
```
$ oc process openshift//jenkins-persistent | oc apply -f- -n fedora-documentation-build
route.route.openshift.io/jenkins created
persistentvolumeclaim/jenkins created
deploymentconfig.apps.openshift.io/jenkins created
serviceaccount/jenkins created
rolebinding.authorization.openshift.io/jenkins_edit created
service/jenkins-jnlp created
service/jenkins created
```

### 3. Instantiate Pipeline
A build template is provided at applier/templates/build.yml that defines all the resources required to buildthe fedora docs app. It includes:

* A BuildConfig that defines a JenkinsPipelineStrategy build, which will be used to define out pipeline.

```
oc process -f .openshift/templates/build.yml -p APPLICATION_NAME="fedora-docs" -p NAMESPACE=fedora-documentation-build -p SOURCE_REPOSITORY_URL="https://pagure.io/fedora-docs-cicd" -p APPLICATION_SOURCE_REPO="https://pagure.io/fedora-docs/docs-fp-o" | oc apply -f-
imagestream.image.openshift.io/fedora-docs created
buildconfig.build.openshift.io/fedora-docs-pipeline configured
buildconfig.build.openshift.io/fedora-docs created
```

### Cleanup
`$ oc delete project fedora-documentation-build fedora-documentation-stage fedora-documentation-prod`

### Reference
[Red Hat Communities of Practice](https://github.com/redhat-cop/container-pipelines/tree/master/basic-spring-boot)
