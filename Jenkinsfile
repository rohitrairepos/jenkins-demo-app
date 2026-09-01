pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        APP_NAME = 'jenkins-demo-app'
        JFROG_REGISTRY = credentials('jfrog-registry-url')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Unit Tests') {
            steps {
                sh 'python3 -m unittest discover -v'
            }
        }

        stage('Lint') {
            steps {
                sh 'python3 -m py_compile app.py test_app.py'
            }
        }

        stage('Docker Build - PR Validation') {
            when {
                changeRequest()
            }
            steps {
                sh 'docker build -t ${APP_NAME}:pr-${BUILD_NUMBER} .'
                sh 'docker image inspect ${APP_NAME}:pr-${BUILD_NUMBER} >/dev/null'
            }
        }

        stage('Determine Release Version') {
            when {
                branch 'master'
            }
            steps {
                script {
                    sh 'git fetch --tags --force'
                    def latestTag = sh(
                        script: "git tag --list 'v*' --sort=-version:refname | head -n 1",
                        returnStdout: true
                    ).trim()

                    if (!latestTag) {
                        env.RELEASE_VERSION = 'v1.0.0'
                    } else {
                        def version = latestTag.replaceFirst(/^v/, '').tokenize('.')
                        def major = version[0] as int
                        def minor = version[1] as int
                        def patch = version[2] as int
                        env.RELEASE_VERSION = "v${major}.${minor}.${patch + 1}"
                    }

                    echo "Release version: ${env.RELEASE_VERSION}"
                }
            }
        }

        stage('Build Release Image') {
            when {
                branch 'master'
            }
            steps {
                sh 'docker build -t ${JFROG_REGISTRY}/${APP_NAME}:${RELEASE_VERSION} .'
            }
        }

        stage('Push Image to JFrog') {
            when {
                branch 'master'
            }
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'artifactory-creds',
                        usernameVariable: 'ARTIFACTORY_USER',
                        passwordVariable: 'ARTIFACTORY_PASSWORD'
                    )
                ]) {
                    sh '''
                        set +x
                        echo "$ARTIFACTORY_PASSWORD" | docker login "$JFROG_REGISTRY" \
                            --username "$ARTIFACTORY_USER" --password-stdin
                        docker push "$JFROG_REGISTRY/$APP_NAME:$RELEASE_VERSION"
                        docker logout "$JFROG_REGISTRY"
                    '''
                }
            }
        }

        stage('Create GitHub Tag') {
            when {
                branch 'master'
            }
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'github-token',
                        usernameVariable: 'GIT_USERNAME',
                        passwordVariable: 'GIT_TOKEN'
                    )
                ]) {
                    sh '''
                        set +x
                        git config user.name "jenkins"
                        git config user.email "jenkins@localhost"
                        git tag -a "$RELEASE_VERSION" -m "Release $RELEASE_VERSION"
                        git remote set-url origin "https://${GIT_USERNAME}:${GIT_TOKEN}@github.com/rohitrairepos/jenkins-demo-app.git"
                        git push origin "$RELEASE_VERSION"
                    '''
                }
            }
        }
    }

    post {
        always {
            sh 'docker image prune -f || true'
        }
    }
}
