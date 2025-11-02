pipeline {
    agent any
    options {
        // 禁止并发构建
        disableConcurrentBuilds()
        // 保留构建日志
        buildDiscarder(logRotator(numToKeepStr: '10'))
        // 控制台高亮输出
        ansiColor('xterm')
    }

    environment {
        PATH = "$PATH:/usr/local/bin"
        PROJECT_DIR = "meiduo"      // 你的项目主目录
        BACKEND_DIR = "meiduo_mall" // Django 后端目录
        FRONTEND_DIR = "meiduo_mall_frontend" // Vue 前端目录
    }

    stages {

        stage("关闭旧容器") {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    echo "================== 🧹 关闭旧容器 =================="
                    sh "cd ${PROJECT_DIR} && docker-compose down || true"
                }
            }
        }

        stage("环境清理") {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    echo "================== 🧼 清理无用镜像与容器 =================="
                    sh '''
                    docker ps -aqf "status=exited" | xargs -r docker rm
                    docker images -qf "dangling=true" | xargs -r docker rmi
                    '''
                }
            }
        }

        stage("构建后端镜像") {
            steps {
                echo "================== 🏗️ 构建后端服务器 =================="
                sh """
                    cd ${PROJECT_DIR}/${BACKEND_DIR}
                    docker build -t meiduo_server:latest .
                """
            }
        }

        stage("构建前端镜像") {
            steps {
                echo "================== 🏗️ 构建前端服务器 =================="
                sh """
                    cd ${PROJECT_DIR}/${FRONTEND_DIR}
                    docker build -t meiduo_web:latest .
                """
            }
        }

        stage("启动服务") {
            steps {
                echo "================== 🚀 启动 docker-compose 服务 =================="
                sh """
                    cd ${PROJECT_DIR}
                    docker-compose up -d --build
                    docker ps
                """
            }
        }
    }

    post {
        success {
            echo "✅ 部署成功：服务已启动"
        }
        failure {
            echo "❌ 部署失败：请检查日志"
        }
        always {
            echo "================== 📜 构建日志路径 =================="
            sh "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"
        }
    }
}

