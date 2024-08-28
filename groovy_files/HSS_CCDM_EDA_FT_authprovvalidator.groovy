pipelineJob('HSS_CCDM_EDA_FT_authprovvalidator') {
    properties {
        allowBrokenBuildClaiming()
    }

    concurrentBuild(false)
    parameters {
        stringParam ('GERRIT_BRANCH', 'master', 'Use this parameter to select your repository BRANCH.')
        stringParam ('GERRIT_REFSPEC', 'master', 'Use same value as GERRIT_BRANCH.')
        stringParam ('GERRIT_BRANCH_FTFW', 'master', 'Use this parameter to select the ftfw BRANCH.')
        stringParam ('CHART_NAME', 'eric-ccdm-eda', 'Use this parameter to select the Helm chart to deploy.')
        stringParam ('CHART_VERSION', '', 'Use this parameter to select the Helm chart version to deploy.')
        stringParam ('CHART_REPO', '', 'Use this parameter to select the Helm repository where the chart is hosted.')
    }

    triggers {
        gerrit {
            events {
                patchsetCreated()
            }

            project('plain:HSS/CCDM/EDA/ft', ['ANT:**'])

            configure { gerritTrigger ->
                new groovy.util.Node(gerritTrigger, 'serverName', 'adp')
                def gerritProjects = gerritTrigger.getAt ('gerritProjects')[0]
                def gerritProject = gerritProjects.getAt ('com.sonyericsson.hudson.plugins.gerrit.trigger.hudsontrigger.data.GerritProject')[0]
                filePaths = new groovy.util.Node (gerritProject, 'filePaths')
                filePath = new groovy.util.Node (filePaths, 'com.sonyericsson.hudson.plugins.gerrit.trigger.hudsontrigger.data.FilePath')
                new groovy.util.Node (filePath, 'compareType', 'plain')
                new groovy.util.Node (filePath, 'pattern', 'Jenkinsfile.HSS_CCDM_EDA_FT_authprovvalidator/**')
                new groovy.util.Node (filePath, compareType, ANT)
                new groovy.util.Node (filePath, 'pattern', 'iwk_5g_to_4g/**')
                new groovy.util.Node (filePath, compareType, ANT)
                new groovy.util.Node (filePath, 'pattern', 'amf_patch/**')

                def skipVoteOnSuccessful = gerritTrigger / 'skipVote' / 'onSuccessful'
                skipVoteOnSuccessful.setValue(false)

                def skipVoteOnFailed = gerritTrigger / 'skipVote' / 'onFailed'
                skipVoteOnFailed.setValue(true)

                def skipVoteOnUnstable = gerritTrigger / 'skipVote' / 'onUnstable'
                skipVoteOnUnstable.setValue(true)

                def skipVoteOnNotBuilt = gerritTrigger / 'skipVote' / 'onNotBuilt'
                skipVoteOnNotBuilt.setValue(true)
            }

            buildSuccessful(null, null)
        }
    }

    definition {
        cpsScm {
            scm {
                git {
                    remote {
                        url ('https://madridci@gerritmirror-ha.lmera.ericsson.se/a/HSS/CCDM/EDA/ft')
                        credentials ('userpwd-hss')
                        branch('${GERRIT_BRANCH}')
                        refspec('${GERRIT_REFSPEC}')
                    }
                    extensions {
                        choosingStrategy {
                            gerritTrigger()
                        }
                        wipeOutWorkspace()
                    }
                }
                lightweight (false)
                scriptPath ('Jenkinsfile.HSS_CCDM_EDA_FT_authprovvalidator')
            }
        }
    }
}
