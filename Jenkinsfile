#!groovy


def version, revision1

node('master') {
    stage ('Checkout')
        checkout scm
    stage ('Build image')
        sh "docker build -t tax_crawl_app:${BUILD_NUMBER} -f Dockerfile ."
    stage ('Image push')
    stage('Remove local images')
        sh("docker rmi -f tax_crawl_app:${BUILD_NUMBER} || :")
    stage('Stop old container')
        sh("docker ps -f name=tax_crawl_linux_test -q | xargs --no-run-if-empty docker container stop")
        sh("docker container ls -a -fname=tax_crawl_linux_test -q | xargs -r docker container rm")
    stage('Deploy test')
}