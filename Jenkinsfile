#!groovy
@Library(["cop-pipeline-step"]) _
node {
    cleanWs()
}
def twistlockConfig = [
    twistlockstaticscan: [
        action                         : "scan",
        twistlockScanTarget            : "<containerImagePlaceholder>", // this value is replaced during twistlock pipeline step
        twistlockProjectName           : 'tmallsnapshotv2-fibers',
        twistlockProjectId             : "move.mp-fibers",
        twistlockSdb                   : "app/mp-common/twistlock",
        twistlockAuthHost              : "api.twistlock.sec.nikecloud.com",
        twistlockConsoleHost           : "twistlock.sec.nikecloud.com",
        twistlockRole                  : "ci",
        //cerberusEnv                    : "china",
        reportDir                      : "build/reports/twistlock",
    ]
]

def getJenkinsAgent(params) {
    if ('china'.equalsIgnoreCase(params.region)) {
        return 'china'
    }
    return ''
}

def getConfigFileName(params) {
    return 'config' + '-' + params.region + '.yml'
}

def getServerlessFileName(params) {
    return 'serverless' + '-' + params.region + '.yml'
}

def getDockerDeployFileName(params) {
    return 'docker-deploy' + '-' + params.region + '.sh'
}

def getProfileData(params) {
    return "-Dspring.profiles.include=${params.stack}-${params.region}"
}
pipeline {
    //agent any
    agent {
        label "${getJenkinsAgent(params)}"
    }
    environment {
       HOME="."
       //DEFAULT_ECR_IMAGE = "$GIT_COMMIT-$BUILD_NUMBER"
    }
    parameters {
        choice(name: 'stack', choices: 'dev\ntest\nprod', description: 'Stack to deploy')
        choice(name: 'region', choices: 'china\nROW', description: 'Aws region to be deployed')
        string(name: 'ecrImageTag', description: 'Docker Container Tag (commit hash or latest)', defaultValue: '')
        choice(name: 'deployAction', choices: 'deploy\nremove', description: 'Deployment action. Choose whether to deploy or remove the stack')
        booleanParam(name: 'deployOverride', defaultValue: false, description: 'Force Deploy (used for deploying non-main branches)')
    }
    options {
        timestamps()
        ansiColor('xterm')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }
    stages {
        stage('Build, Test, and Deploy Docker Image') {
            when {
                expression { params.deployAction == 'deploy' }
            }
            steps {
                script {
                    def readContent = readFile 'Dockerfile'
                    writeFile file: 'Dockerfile', text: readContent + "\nENTRYPOINT [\"java\", \"${getProfileData(params)}\" ,\"-jar\",\"/app/spring-boot-application.jar\"]"

                    CONFIG = readYaml(file: "${getConfigFileName(params)}")
                    SERVERLESS_CONFIG = readYaml(file: "${getServerlessFileName(params)}")

                    // Grab Nike CA Certs
                    sh 'cp /etc/ssl/certs/java/cacerts cacerts'

                   // withAWS(region: "${CONFIG[params.stack].awsRegion}", roleAccount: "${CONFIG[params.stack].awsAccountNumber}", role: "${CONFIG[params.stack].jenkinsRoleName}") {
                       // sh "${WORKSPACE}/docker-deploy-china.sh -s ${SERVERLESS_CONFIG.service} -a ${CONFIG[params.stack].awsAccountNumber} -r ${CONFIG[params.stack].awsRegion} -t ${ params.ecrImageTag ? params.ecrImageTag : GIT_COMMIT }"
                    withAWS(region: "${CONFIG[params.stack].awsRegion}", roleAccount: "${CONFIG[params.stack].awsAccountNumber}", role: "${CONFIG[params.stack].jenkinsRoleName}") {
                        sh "${WORKSPACE}/${getDockerDeployFileName(params)} -s ${SERVERLESS_CONFIG.service} -a ${CONFIG[params.stack].awsAccountNumber} -r ${CONFIG[params.stack].awsRegion} -t ${ params.ecrImageTag ? params.ecrImageTag : GIT_COMMIT }"

                    }
                }
            }
        }
//        stage('Twistlock Container Scan') {
//            when {
//                expression { params.deployAction == 'deploy' }
//            }
//            steps {
//                script {
//                    CONFIG = readYaml (file: 'config-china.yml')
//                    SERVERLESS_CONFIG = readYaml (file: 'serverless-china.yml')
//                    Config.staticscan.ScanTarget = "${CONFIG[params.stack].awsAccountNumber}.dkr.ecr.${CONFIG[params.stack].awsRegion}.amazonaws.com.cn/${SERVERLESS_CONFIG.service}:${ params.ecrImageTag ? params.ecrImageTag : DEFAULT_ECR_IMAGE }"
                     // Config.staticscan.ScanTarget = "......dkr.ecr.${CONFIG[params.stack].awsRegion}.amazonaws.com.cn/${SERVERLESS_CONFIG.service}..."

//                }
//                StaticScan(Config.staticscan)
//            }
//        }
        stage('QMA') {
            when {
                expression { params.deployAction == 'deploy' }
            }
            steps {
                qma(twistlockConfig + [action: 'create'])
                qma(twistlockConfig + [action: 'submit', phase: 'build'])
                qma(twistlockConfig + [action: 'check', phase: 'build'])
                qma(twistlockConfig + [action: 'submit', phase: 'twistlock_scan'])
            }
        }
        stage('Deploy ECS - Fargate Resources') {
            environment {
                appScenario= "${params.appScenario}"
                ecrImageTag= "${params.ecrImageTag ? params.ecrImageTag : GIT_COMMIT}"
            }
            agent {
                docker {
                    image 'artifactory.nike.com:9002/mp-aws/docker-container-buildv2:latest'
                    label "${getJenkinsAgent(params)}"
                }
            }
            when {
                anyOf {
                    branch 'main'
                    expression { return (params.deployOverride) }
                }
            }
            steps {
                script {
                    sh 'npm config set @nike:registry=http://artifactory.nike.com/artifactory/api/npm/npm-nike/'
                    sh 'npm ci --loglevel warn'

                    CONFIG = readYaml(file: "${getConfigFileName(params)}")
                    withAWS(region: "${CONFIG[params.stack].awsRegion}", roleAccount: "${CONFIG[params.stack].awsAccountNumber}", role: "${CONFIG[params.stack].jenkinsRoleName}") {
                        echo "Deploying to ${CONFIG[params.stack].awsRegion} / ${params.stack}..."
                        sh "npx serverless ${params.deployAction} --region ${CONFIG[params.stack].awsRegion} --stage ${params.stack} --verbose --config ${getServerlessFileName(params)}"
                    }
                }
            }
        }
    }
//    post {
//        success {
//            slackSend channel: 'mp-perseus-bmx', color: 'good', message: "Deploy Complete - ${params.stack} - ${currentBuild.fullDisplayName} (<${env.RUN_DISPLAY_URL}|Open>)"
//        }
//        failure {
//            slackSend channel: 'mp-perseus-bmx', color: 'danger', message: "Build/Deploy Failed - ${params.stack} - ${currentBuild.fullDisplayName} (<${env.RUN_DISPLAY_URL}|Open>)"
//        }
//    }
}
