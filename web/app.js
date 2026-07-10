const splashScreen = document.getElementById("splashScreen");
const astraPixels = document.getElementById("astraPixels");
const enterAstraBtn = document.getElementById("enterAstraBtn");
const skipAstraBtn = document.getElementById("skipAstraBtn");
const loginScreen = document.getElementById("loginScreen");
const appShell = document.getElementById("appShell");
const signinEmailInput = document.getElementById("signinEmail");
const signinPasswordInput = document.getElementById("signinPassword");
const loadProfileBtn = document.getElementById("loadProfileBtn");
const profileStatus = document.getElementById("profileStatus");
const authTitle = document.getElementById("authTitle");
const authSubtitle = document.getElementById("authSubtitle");
const showSigninBtn = document.getElementById("showSigninBtn");
const showSignupBtn = document.getElementById("showSignupBtn");
const signinPanel = document.getElementById("signinPanel");
const signupPanel = document.getElementById("signupPanel");
const signupName = document.getElementById("signupName");
const signupEmail = document.getElementById("signupEmail");
const signupPassword = document.getElementById("signupPassword");
const signupStudentName = document.getElementById("signupStudentName");
const signupHours = document.getElementById("signupHours");
const signupWhyAstra = document.getElementById("signupWhyAstra");
const signupInterests = document.getElementById("signupInterests");
const signupDislikes = document.getElementById("signupDislikes");
const signupConversationStyle = document.getElementById("signupConversationStyle");
const signupStressSupport = document.getElementById("signupStressSupport");
const signupGoalsSummary = document.getElementById("signupGoalsSummary");
const openSignupWalkthroughBtn = document.getElementById("openSignupWalkthroughBtn");
const skipSignupWalkthroughBtn = document.getElementById("skipSignupWalkthroughBtn");
const createProfileBtn = document.getElementById("createProfileBtn");
const studentWelcome = document.getElementById("studentWelcome");
const studentSubcopy = document.getElementById("studentSubcopy");
const avatarGrid = document.getElementById("avatarGrid");
const sidebarTutorSummary = document.getElementById("sidebarTutorSummary");
const dataSaveStatus = document.getElementById("dataSaveStatus");
const dataSaveCounts = document.getElementById("dataSaveCounts");
const leagueName = document.getElementById("leagueName");
const leaguePoints = document.getElementById("leaguePoints");
const leagueNext = document.getElementById("leagueNext");
const leagueProgressFill = document.getElementById("leagueProgressFill");
const leagueMissions = document.getElementById("leagueMissions");
const leagueRecent = document.getElementById("leagueRecent");
const leagueTabName = document.getElementById("leagueTabName");
const leagueTabPoints = document.getElementById("leagueTabPoints");
const leagueTabStreak = document.getElementById("leagueTabStreak");
const leagueTabNext = document.getElementById("leagueTabNext");
const leagueTabProgressFill = document.getElementById("leagueTabProgressFill");
const leagueTabLadder = document.getElementById("leagueTabLadder");
const leagueTabMissions = document.getElementById("leagueTabMissions");
const leagueTabRecent = document.getElementById("leagueTabRecent");
const miniLeagueTier = document.getElementById("mini-league-tier");
const miniLeagueLP = document.getElementById("mini-league-lp");
const motivationQuickAccessBtn = document.getElementById("motivationQuickAccessBtn");
const dailyMotivationQuote = document.getElementById("dailyMotivationQuote");
const motivationBoostTokens = document.getElementById("motivationBoostTokens");
const motivationStoryStatus = document.getElementById("motivationStoryStatus");
const motivationStoryTitle = document.getElementById("motivationStoryTitle");
const motivationStoryBody = document.getElementById("motivationStoryBody");
const motivationReadStoryBtn = document.getElementById("motivationReadStoryBtn");
const motivationPrevStoryBtn = document.getElementById("motivationPrevStoryBtn");
const motivationNextStoryBtn = document.getElementById("motivationNextStoryBtn");
const motivationSection = document.getElementById("motivationSection");
const talkToAstraInLoungeBtn = document.getElementById("talkToAstraInLoungeBtn");
const tutorNameInput = document.getElementById("tutorNameInput");
const saveTutorNameBtn = document.getElementById("saveTutorNameBtn");
const tutorPersonaPresetSelect = document.getElementById("tutorPersonaPresetSelect");
const tutorStyleInput = document.getElementById("tutorStyleInput");
const tutorAppearanceInput = document.getElementById("tutorAppearanceInput");
const tutorTraitChips = document.getElementById("tutorTraitChips");
  const tutorStudioSummary = document.getElementById("tutorStudioSummary");
  const avatarStageTitle = document.getElementById("avatarStageTitle");
  const avatarStageTagline = document.getElementById("avatarStageTagline");
  const avatarStageStatus = document.getElementById("avatarStageStatus");
  const avatarStageContainer = document.getElementById("avatar-stage-container");
  const avatarCanvas = document.getElementById("avatar-canvas");
  const avatarSpeakBtn = document.getElementById("avatar-speak-btn");
  const avatarStopBtn = document.getElementById("avatar-stop-btn");
  const avatarStatusText = document.getElementById("avatar-status-text");
  const avatarNameBadge = document.getElementById("avatar-name-badge");
  const avatarFace = document.getElementById("avatarFace");
  const avatarPortrait = document.getElementById("avatarPortrait");
  const avatarMouth = document.getElementById("avatarMouth");
  const avatarGlasses = document.getElementById("avatarGlasses");
  const avatarShoulders = document.getElementById("avatarShoulders");
const avatarAppearanceText = document.getElementById("avatarAppearanceText");
const chapterResumeBanner = document.getElementById("chapter-resume-banner");
const chapterResumeCard = document.getElementById("chapter-resume-card");
const chapterDetailCloseBtn = document.getElementById("chapterDetailCloseBtn");
const chapterCompletionCard = document.getElementById("chapter-completion-card");
const chapterTestContainer = document.getElementById("chapter-test-container");
const refreshWeeklyPlanBtn = document.getElementById("refreshWeeklyPlanBtn");
const refreshWeeklyPlanBtnAlt = document.getElementById("refreshWeeklyPlanBtnAlt");
const openWeeklyTabBtn = document.getElementById("openWeeklyTabBtn");
const openProgressTabBtn = document.getElementById("openProgressTabBtn");
const jumpToTutorBtn = document.getElementById("jumpToTutorBtn");
const viewAllTutorChatsBtn = document.getElementById("viewAllTutorChatsBtn");
const closeTutorConversationDrawerBtn = document.getElementById("closeTutorConversationDrawerBtn");
const tutorConversationDrawer = document.getElementById("tutorConversationDrawer");
const tutorConversationDrawerBackdrop = document.getElementById("tutorConversationDrawerBackdrop");
const tutorConversationDrawerToday = document.getElementById("tutorConversationDrawerToday");
const tutorConversationDrawerYesterday = document.getElementById("tutorConversationDrawerYesterday");
const tutorConversationDrawerWeek = document.getElementById("tutorConversationDrawerWeek");
const tutorConversationDrawerOlder = document.getElementById("tutorConversationDrawerOlder");
const logoutBtn = document.getElementById("logoutBtn");
const studioMenuToggleBtn = document.getElementById("studioMenuToggleBtn");
const languageBadge = document.getElementById("languageBadge");
const tutorModeBadge = document.getElementById("tutorModeBadge");
const tutorModePill = document.getElementById("tutorModePill");
const tutorModeButtons = Array.from(document.querySelectorAll("[data-tutor-mode]"));
const tutorLevelSelect = document.getElementById("tutorLevelSelect");
const tutorLevelHint = document.getElementById("tutorLevelHint");
const adaptiveProfileNote = document.getElementById("adaptiveProfileNote");
const journeySetupCard = document.getElementById("journey-setup-card");
const journeyExamDateInput = document.getElementById("journey-exam-date");
const journeyHoursInput = document.getElementById("journeyHoursInput");
const journeyHoursLabel = document.getElementById("journeyHoursLabel");
const setupJourneyBtn = document.getElementById("setupJourneyBtn");
const journeyExamDateSaveBtn = document.getElementById("journeyExamDateSaveBtn");
const beginJourneyBtn = document.getElementById("beginJourneyBtn");
const journeySetupStatus = document.getElementById("journeySetupStatus");
const todaysFocusCard = document.getElementById("todays-focus-card");
const todaysFocusSummary = document.getElementById("todaysFocusSummary");
const todaysSessionBadge = document.getElementById("todaysSessionBadge");
const todaysSubjectBadge = document.getElementById("todaysSubjectBadge");
const todaysUnitText = document.getElementById("todaysUnitText");
const todaysTopicText = document.getElementById("todaysTopicText");
const todaysConfidenceText = document.getElementById("todaysConfidenceText");
const todaysWeightageText = document.getElementById("todaysWeightageText");
const todaysGoalText = document.getElementById("todaysGoalText");
const startSessionBtn = document.getElementById("startSessionBtn");
const openJourneySummaryBtn = document.getElementById("openJourneySummaryBtn");
const sessionTimerCard = document.getElementById("session-timer");
const sessionTimerPill = document.getElementById("sessionTimerPill");
const sessionTimerText = document.getElementById("sessionTimerText");
const sessionSummaryCard = document.getElementById("session-summary-card");
const sessionSummaryText = document.getElementById("sessionSummaryText");
const sessionSummaryBadge = document.getElementById("sessionSummaryBadge");
const sessionScoreText = document.getElementById("sessionScoreText");
const sessionNextRevisionText = document.getElementById("sessionNextRevisionText");
const sessionTomorrowText = document.getElementById("sessionTomorrowText");
const journeyProgressSidebar = document.getElementById("journey-progress-sidebar");
const journeyCoveredText = document.getElementById("journeyCoveredText");
const journeyStreakText = document.getElementById("journeyStreakText");
const journeyOverallText = document.getElementById("journeyOverallText");
const journeyMilestoneText = document.getElementById("journeyMilestoneText");
const journeyMasteryCard = document.getElementById("journey-mastery-card");
const journeyMasterySummary = document.getElementById("journeyMasterySummary");
const journeyMasteryList = document.getElementById("journeyMasteryList");
const weeklyCoreHours = document.getElementById("weeklyCoreHours");
const weeklyScheduledHours = document.getElementById("weeklyScheduledHours");
const weeklyFocusSplit = document.getElementById("weeklyFocusSplit");
const weeklyPlanTableBody = document.querySelector("#weeklyPlanTable tbody");
const weeklyPreviewCards = document.getElementById("weeklyPreviewCards");
const sectionProgressList = document.getElementById("sectionProgressList");
const planSubjectBreakdownList = document.getElementById("planSubjectBreakdownList");
const weeklyStrategyList = document.getElementById("weeklyStrategyList");
const memorySummary = document.getElementById("memorySummary");
const studentInsightSummary = document.getElementById("studentInsightSummary");
const overviewTodayText = document.getElementById("overviewTodayText");
const overviewWeekText = document.getElementById("overviewWeekText");
const overviewNextText = document.getElementById("overviewNextText");
const dailyBriefingCard = document.getElementById("dailyBriefingCard");
const dailyBriefingText = document.getElementById("dailyBriefingText");
const dismissDailyBriefingBtn = document.getElementById("dismissDailyBriefingBtn");
const astraStatusBar = document.getElementById("astra-status-bar");
const sessionStatsCard = document.getElementById("session-stats-card");
const sessionStatsTopic = document.getElementById("sessionStatsTopic");
const sessionStatsConfidence = document.getElementById("sessionStatsConfidence");
const sessionStatsCount = document.getElementById("sessionStatsCount");
const sessionStatsAverage = document.getElementById("sessionStatsAverage");
const sessionStatsStreak = document.getElementById("sessionStatsStreak");
const tutorSmartPromptLine = document.getElementById("tutorSmartPromptLine");
const tutorSmartPromptChips = document.getElementById("tutorSmartPromptChips");
const sessionActivityPanel = document.getElementById("session-activity-panel");
const sessionActivityToggleBtn = document.getElementById("sessionActivityToggleBtn");
const sessionActivityList = document.getElementById("sessionActivityList");
const overviewCommandTopic = document.getElementById("overviewCommandTopic");
const overviewCommandBadge = document.getElementById("overviewCommandBadge");
const overviewCommandReason = document.getElementById("overviewCommandReason");
const overviewCommandSubject = document.getElementById("overviewCommandSubject");
const overviewCommandTime = document.getElementById("overviewCommandTime");
const overviewCommandWhy = document.getElementById("overviewCommandWhy");
const overviewStartLearningBtn = document.getElementById("overviewStartLearningBtn");
const overviewMetricCovered = document.getElementById("overviewMetricCovered");
const overviewMetricAverage = document.getElementById("overviewMetricAverage");
const overviewMetricStreak = document.getElementById("overviewMetricStreak");
const overviewLastTopic = document.getElementById("overviewLastTopic");
const overviewLastTopicStatus = document.getElementById("overviewLastTopicStatus");
const overviewProgressBadge = document.getElementById("overviewProgressBadge");
const overviewDoneCount = document.getElementById("overviewDoneCount");
const overviewReviseCount = document.getElementById("overviewReviseCount");
const overviewPendingCount = document.getElementById("overviewPendingCount");
const overviewNextStep = document.getElementById("overviewNextStep");
const continueJourneyBtn = document.getElementById("continueJourneyBtn");
const openPracticeFromHomeBtn = document.getElementById("openPracticeFromHomeBtn");
const needHelpConceptBtn = document.getElementById("needHelpConceptBtn");
const openProgressFromHomeBtn = document.getElementById("openProgressFromHomeBtn");
const walkthroughModal = document.getElementById("walkthroughModal");
const walkthroughBackdrop = walkthroughModal ? walkthroughModal.querySelector(".walkthrough-backdrop") : null;
const walkthroughParticles = document.getElementById("walkthroughParticles");
const walkthroughQuestionBlock = document.getElementById("walkthroughQuestionBlock");
const walkthroughAstraNote = document.getElementById("walkthroughAstraNote");
const walkthroughModePill = document.getElementById("walkthroughModePill");
const walkthroughStepLabel = document.getElementById("walkthroughStepLabel");
const walkthroughStepCount = document.getElementById("walkthroughStepCount");
const walkthroughPrompt = document.getElementById("walkthroughPrompt");
const walkthroughHelper = document.getElementById("walkthroughHelper");
const walkthroughInput = document.getElementById("walkthroughInput");
const walkthroughAstraAnswer = document.getElementById("walkthroughAstraAnswer");
const walkthroughBackBtn = document.getElementById("walkthroughBackBtn");
const walkthroughSkipBtn = document.getElementById("walkthroughSkipBtn");
const walkthroughNextBtn = document.getElementById("walkthroughNextBtn");
const walkthroughSaveBtn = document.getElementById("walkthroughSaveBtn");
const walkthroughCloseBtn = document.getElementById("walkthroughCloseBtn");
const askAstraBtn = document.getElementById("askAstraBtn");
const startWalkWithAstraBtn = document.getElementById("startWalkWithAstraBtn");
const editWalkWithAstraBtn = document.getElementById("editWalkWithAstraBtn");
const memoryManager = document.getElementById("memoryManager");
const funFactText = document.getElementById("funFactText");
const funFactCategory = document.getElementById("funFactCategory");
const liveSourcesList = document.getElementById("liveSourcesList");
const visualLearningPanel = document.getElementById("visualLearningPanel");
const videoExplanationPanel = document.getElementById("videoExplanationPanel");
const conceptCanvasPanel = document.getElementById("conceptCanvasPanel");
const conceptCanvas = document.getElementById("conceptCanvas");
const reasoningPanel = document.getElementById("reasoningPanel");
const summaryPanel = document.getElementById("summaryPanel");
const videoTutorWeeklyStatus = document.getElementById("videoTutorWeeklyStatus");
const videoTutorWeeklyVideos = document.getElementById("videoTutorWeeklyVideos");
const videoTutorRequestTopicInput = document.getElementById("video-topic-search") || document.getElementById("videoTutorRequestTopicInput");
const videoTutorRequestSubjectSelect = document.getElementById("video-subject-select") || document.getElementById("videoTutorRequestSubjectSelect");
const generateRequestedVideoBtn = document.getElementById("video-search-generate-btn") || document.getElementById("generateRequestedVideoBtn");
const videoTutorRequestStatus = document.getElementById("videoTutorRequestStatus");
const videoTutorRequestBriefPanel = document.getElementById("videoTutorRequestBriefPanel");
const generateRequestedFullVideoBtn = document.getElementById("generateRequestedFullVideoBtn");
const videoTutorRequestedList = document.getElementById("videoTutorRequestedList");
const videoTutorQuestionInput = document.getElementById("videoTutorQuestionInput");
const generateVideoAnswerBtn = document.getElementById("generateVideoAnswerBtn");
const videoAnswerBtn = document.getElementById("videoAnswerBtn");
const videoAnswerBriefPanel = document.getElementById("videoAnswerBriefPanel");
const videoStatusPanel = document.getElementById("video-status-panel");
const tutorVideoAnswerPlayer = document.getElementById("tutor-video-answer-player") || document.getElementById("tutor-video-player");
const tutorVideoPlayer = document.getElementById("tutorVideoPlayer") || document.getElementById("tutor-video-player");
const videoTranscriptPanel = document.getElementById("video-transcript");
const videoRenderStatus = document.getElementById("videoRenderStatus");
const videoQuestionInput = videoTutorQuestionInput;
const videoSubjectSelect = videoTutorRequestSubjectSelect;
const tutorVideoTitle = document.getElementById("tutorVideoTitle");
const tutorVideoMeta = document.getElementById("tutorVideoMeta");
const tutorVideoSummary = document.getElementById("tutorVideoSummary");
const tutorVideoBridgeCues = document.getElementById("tutorVideoBridgeCues");
const tutorVideoList = document.getElementById("tutorVideoList");
const openVideoBridgeBtn = document.getElementById("openVideoBridgeBtn");
const useVideoInTutorBtn = document.getElementById("useVideoInTutorBtn");
const vtCurrentTopicCard = null;
const vtTopicName = null;
const vtTopicSubject = null;
const vtSuggestedChips = null;
const vtWeekRow = null;
const vtLibraryGrid = null;
const vtStatusPanel = null;
const vtStatusText = null;
const chatFeed = document.getElementById("chatFeed");
const kbStatusTag = document.getElementById("kbStatusTag");
const guideFeed = document.getElementById("guideFeed");
const loungeFeed = document.getElementById("loungeFeed");
const practiceFeed = document.getElementById("practiceFeed");
const clearTutorChatBtn = document.getElementById("clearTutorChatBtn");
const tutorFullscreenBtn = document.getElementById("tutor-fullscreen-btn");
const loungeFullscreenBtn = document.getElementById("lounge-fullscreen-btn");
const clearPracticeChatBtn = document.getElementById("clearPracticeChatBtn");
const clearLoungeChatBtn = document.getElementById("clearLoungeChatBtn");
const newTutorChatBtn = document.getElementById("newTutorChatBtn");
const tutorConversationList = document.getElementById("tutorConversationList");
const deletedTutorConversationList = document.getElementById("deletedTutorConversationList");
const tutorChatSearchInput = document.getElementById("tutorChatSearchInput");
const newLoungeChatBtn = document.getElementById("newLoungeChatBtn");
const loungeTimerToggleBtn = document.getElementById("loungeTimerToggleBtn");
const loungeTimerPanel = document.getElementById("loungeTimerPanel");
const loungeHistoryToggleBtn = document.getElementById("loungeHistoryToggleBtn");
const loungeHistoryPanel = document.getElementById("loungeHistoryPanel");
const closeLoungeHistoryBtn = document.getElementById("closeLoungeHistoryBtn");
const loungeDeletedToggleBtn = document.getElementById("loungeDeletedToggleBtn");
const loungeDeletedPanel = document.getElementById("deletedLoungeConversationList");
const loungeConversationList = document.getElementById("loungeConversationList");
const deletedLoungeConversationList = document.getElementById("deletedLoungeConversationList");
const loungeChatSearchInput = document.getElementById("loungeChatSearchInput");
const loungeConversationSelect = document.getElementById("loungeConversationSelect");
const loungeRenameChatBtn = document.getElementById("loungeRenameChatBtn");
const loungePinChatBtn = document.getElementById("loungePinChatBtn");
const loungeDeleteChatBtn = document.getElementById("loungeDeleteChatBtn");
const deletedLoungeConversationSelect = document.getElementById("deletedLoungeConversationSelect");
const restoreLoungeChatBtn = document.getElementById("restoreLoungeChatBtn");
const lastMinuteFeed = document.getElementById("lastMinuteFeed");
const tipsFeed = document.getElementById("tipsFeed");
const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const summarizeTutorBtn = document.getElementById("summarizeTutorBtn");
const quickSummaryBtn = document.getElementById("quickSummaryBtn");
const tutorRoomForm = document.getElementById("tutorRoomForm");
const tutorRoomMessageInput = document.getElementById("tutorRoomMessageInput");
const tutorRoomLivePill = document.getElementById("tutorRoomLivePill");
const tutorRoomLiveSummary = document.getElementById("tutorRoomLiveSummary");
const tutorRoomLiveHint = document.getElementById("tutorRoomLiveHint");
const tutorRoomVoiceState = document.getElementById("tutorRoomVoiceState");
const tutorRoomSpeakState = document.getElementById("tutorRoomSpeakState");
const tutorRoomCaptionState = document.getElementById("tutorRoomCaptionState");
const tutorRoomReadState = document.getElementById("tutorRoomReadState");
const tutorRoomPaceState = document.getElementById("tutorRoomPaceState");
const tutorRoomLevelState = document.getElementById("tutorRoomLevelState");
const tutorRoomSpeakLastBtn = document.getElementById("tutorRoomSpeakLastBtn");
const tutorRoomPauseBtn = document.getElementById("tutorRoomPauseBtn");
const tutorRoomResumeBtn = document.getElementById("tutorRoomResumeBtn");
const tutorRoomStopBtn = document.getElementById("tutorRoomStopBtn");
const tutorRoomBackToTutorBtn = document.getElementById("tutorRoomBackToTutorBtn");
const tutorRoomTranscriptFeed = document.getElementById("tutorRoomTranscript");
const tutorChatPanel = document.querySelector(".tutor-chat-panel");
const tutorTab = document.getElementById("tutorTab");
const tutorControlsBar = tutorTab ? tutorTab.querySelector(".tutor-controls-bar") : null;
const tutorModeCard = tutorTab ? tutorTab.querySelector(".tutor-mode-card") : null;
const quickPromptGrid = tutorTab ? tutorTab.querySelector(".quick-prompt-grid") : null;
let tutorFullscreenOverlay = null;
let tutorFullscreenMessages = null;
let tutorFullscreenInputArea = null;
let tutorFullscreenTextarea = null;
let tutorFullscreenSendButton = null;
let tutorFullscreenMirrorObserver = null;
let tutorFullscreenMirrorSource = null;
let loungeFullscreenOverlay = null;
let loungeFullscreenMessages = null;
let loungeFullscreenTextarea = null;
let loungeFullscreenMirrorObserver = null;
let loungeFullscreenMirrorSource = null;
let tutorTabLayout = null;
let tutorControlStrip = null;
let tutorChatZone = null;
let tutorSidePanel = null;
let tutorInputZone = null;
let activeTutorSideTab = "session";
let tutorSidePanelCollapsed = false;
const videoApiBaseUrl = window.__ASTRA_VIDEO_API_BASE__ || "http://127.0.0.1:8001";
const doubtImageInput = document.getElementById("doubtImageInput");
const analyzeImageBtn = document.getElementById("analyzeImageBtn");
const imageUploadStatus = document.getElementById("imageUploadStatus");
const loungeForm = document.getElementById("loungeForm");
const loungeMessageInput = document.getElementById("loungeMessageInput");
const loungeVoiceBtn = document.getElementById("loungeVoiceBtn");
const loungeVoiceStatus = document.getElementById("loungeVoiceStatus");
const guideForm = document.getElementById("guideForm");
const guideMessageInput = document.getElementById("guideMessageInput");
const practiceForm = document.getElementById("practiceForm");
const practiceMessageInput = document.getElementById("practiceMessageInput");
const lastMinuteForm = document.getElementById("lastMinuteForm");
const lastMinuteMessageInput = document.getElementById("lastMinuteMessageInput");
const mockTestIntroCard = document.getElementById("mockTestIntroCard");
const startMockTestBtn = document.getElementById("startMockTestBtn");
const mockTestSetupCard = document.getElementById("mockTestSetupCard");
const mockTestExamInput = document.getElementById("mockTestExamInput");
const mockTestCountInput = document.getElementById("mockTestCountInput");
const mockTestTimer = document.getElementById("mockTestTimer");
const mockTestProgress = document.getElementById("mockTestProgress");
const mockTestQuestionCard = document.getElementById("mockTestQuestionCard");
const mockTestQuestionText = document.getElementById("mockTestQuestionText");
const mockTestQuestionMeta = document.getElementById("mockTestQuestionMeta");
const mockTestOptionList = document.getElementById("mockTestOptionList");
const mockTestIntegerInput = document.getElementById("mockTestIntegerInput");
const mockTestNavPrev = document.getElementById("mockTestNavPrev");
const mockTestNavNext = document.getElementById("mockTestNavNext");
const mockTestSubmitBtn = document.getElementById("mockTestSubmitBtn");
const mockTestReportCard = document.getElementById("mockTestReportCard");
const mockTestReportBody = document.getElementById("mockTestReportBody");
const mockTestStatus = document.getElementById("mockTestStatus");
const mockTestWeeklyPlanBtn = document.getElementById("mockTestWeeklyPlanBtn");
const mockTestExitBtn = document.getElementById("mockTestExitBtn");
const mockTestExitBtnReport = document.getElementById("mockTestExitBtnReport");
const mockTestTab = document.getElementById("mockTestTab");
const mockCatalogueList = document.getElementById("mockCatalogueList");
const mockExternalExamType = document.getElementById("mockExternalExamType");
const mockExternalTotalScore = document.getElementById("mockExternalTotalScore");
const mockExternalMaxScore = document.getElementById("mockExternalMaxScore");
const mockExternalPhysicsScore = document.getElementById("mockExternalPhysicsScore");
const mockExternalChemistryScore = document.getElementById("mockExternalChemistryScore");
const mockExternalMathsScore = document.getElementById("mockExternalMathsScore");
const mockExternalTimeTaken = document.getElementById("mockExternalTimeTaken");
const mockExternalNotes = document.getElementById("mockExternalNotes");
const mockExternalAnalyseBtn = document.getElementById("mockExternalAnalyseBtn");
const mockExternalAnalysisResult = document.getElementById("mockExternalAnalysisResult");
const mockHistoryList = document.getElementById("mockHistoryList");
const tipsForm = document.getElementById("tipsForm");
const tipsMessageInput = document.getElementById("tipsMessageInput");
const learningSourcesList = document.getElementById("learningSourcesList");
const learningSourcePackBadge = document.getElementById("learningSourcePackBadge");
const studyGroupsStatus = document.getElementById("studyGroupsStatus");
const refreshStudyGroupsBtn = document.getElementById("refreshStudyGroupsBtn");
const activeGroupSessionPill = document.getElementById("activeGroupSessionPill");
const activeGroupSessionCard = document.getElementById("activeGroupSessionCard");
const groupCandidatesList = document.getElementById("groupCandidatesList");
const groupSessionPanel = document.getElementById("groupSessionPanel");
const groupSessionTitle = document.getElementById("groupSessionTitle");
const groupSessionMeta = document.getElementById("groupSessionMeta");
const groupMainFeed = document.getElementById("groupMainFeed");
const groupMainForm = document.getElementById("groupMainForm");
const groupMainInput = document.getElementById("groupMainInput");
const groupTutorNextBtn = document.getElementById("groupTutorNextBtn");
const groupStepOutBtn = document.getElementById("groupStepOutBtn");
const groupBreakoutPanel = document.getElementById("groupBreakoutPanel");
const groupBreakoutFeed = document.getElementById("groupBreakoutFeed");
const groupBreakoutForm = document.getElementById("groupBreakoutForm");
const groupBreakoutInput = document.getElementById("groupBreakoutInput");
const groupRejoinBtn = document.getElementById("groupRejoinBtn");
const groupVoiceToggle = document.getElementById("groupVoiceToggle");
const refreshProgressBtn = document.getElementById("refreshProgressBtn");
const progressReminderText = document.getElementById("progressReminderText");
const progressWeekSummary = document.getElementById("progressWeekSummary");
const progressDoneCount = document.getElementById("progressDoneCount");
const progressReviseCount = document.getElementById("progressReviseCount");
const progressPendingCount = document.getElementById("progressPendingCount");
const progressTotalCount = document.getElementById("progressTotalCount");
const progressCurrentWeekRate = document.getElementById("progressCurrentWeekRate");
const progressPreviousWeekRate = document.getElementById("progressPreviousWeekRate");
const progressImprovementRate = document.getElementById("progressImprovementRate");
const progressNeedFocus = document.getElementById("progressNeedFocus");
const progressComparisonText = document.getElementById("progressComparisonText");
const progressTrendLensBtn = document.getElementById("progressTrendLensBtn");
const analyticsInsightCard = document.getElementById("analytics-insight-card");
const performanceChartCard = document.getElementById("performance-chart");
const performanceChartSummary = document.getElementById("performanceChartSummary");
const performanceChartBars = document.getElementById("performanceChartBars");
const subjectBreakdownCards = document.getElementById("subject-breakdown-cards");
const subjectBreakdownGrid = document.getElementById("subjectBreakdownGrid");
const consistencyTrackerCard = document.getElementById("consistency-tracker");
const consistencyTrackerSummary = document.getElementById("consistencyTrackerSummary");
const consistencyTrackerGrid = document.getElementById("consistencyTrackerGrid");
const chapterMasteryCard = document.getElementById("chapter-mastery-board") || document.getElementById("chapter-mastery-card");
const chapterMasterySummary = document.getElementById("chapterMasterySummary");
const chapterMasteryGrid = document.getElementById("chapterMasteryGrid");
const chapterAnalyticsCard = document.getElementById("chapter-analytics-card");
const chapterAnalyticsSummary = document.getElementById("chapterAnalyticsSummary");
const chapterAnalyticsList = document.getElementById("chapterAnalyticsList");
const analyticsDashboardBtn = document.getElementById("analyticsDashboardBtn");
const chapterRevisionCard = document.getElementById("chapter-revision-card");
const chapterRevisionSummary = document.getElementById("chapterRevisionSummary");
const chapterRevisionList = document.getElementById("chapterRevisionList");
const chapterDetailCard = document.getElementById("chapter-detail-card");
const chapterDetailSummary = document.getElementById("chapterDetailSummary");
const chapterDetailList = document.getElementById("chapterDetailList");
const formulasSearchInput = document.getElementById("formulasSearchInput");
const formulaSubjectButtons = Array.from(document.querySelectorAll("[data-formula-subject]"));
const formulasWeakToggle = document.getElementById("formulasWeakToggle");
const formulasChapterToggle = document.getElementById("formulasChapterToggle");
const formulasChapterToggleText = document.getElementById("formulasChapterToggleText");
const formulasChapterDropdownPanel = document.getElementById("formulasChapterDropdownPanel");
const formulasChapterList = document.getElementById("formulasChapterList");
const formulasStatus = document.getElementById("formulasStatus");
const formulasChapterSubject = document.getElementById("formulasChapterSubject");
const formulasChapterTitle = document.getElementById("formulasChapterTitle");
const formulasWeightageChip = document.getElementById("formulasWeightageChip");
const formulasFormulaList = document.getElementById("formulasFormulaList");
const formulasShortcutList = document.getElementById("formulasShortcutList");
const formulasMistakeList = document.getElementById("formulasMistakeList");
const formulasDownloadBtn = document.getElementById("formulasDownloadBtn");
const startChapterSessionBtn = document.getElementById("startChapterSessionBtn");
const progressWeeklyCanvas = document.getElementById("progressWeeklyCanvas");
const progressExamInput = document.getElementById("progressExamInput");
const progressSubjectInput = document.getElementById("progressSubjectInput");
const progressTopicInput = document.getElementById("progressTopicInput");
const progressStatusSelect = document.getElementById("progressStatusSelect");
const progressNoteInput = document.getElementById("progressNoteInput");
const saveProgressItemBtn = document.getElementById("saveProgressItemBtn");
const progressDoneList = document.getElementById("progressDoneList");
const progressReviseList = document.getElementById("progressReviseList");
const progressPendingList = document.getElementById("progressPendingList");
const loungeTimerStatus = document.getElementById("loungeTimerStatus");
const stopLoungeTimerBtn = document.getElementById("stopLoungeTimerBtn");
const personManagerInput = document.getElementById("personManagerInput");
const addPersonBtn = document.getElementById("addPersonBtn");
const interestManagerInput = document.getElementById("interestManagerInput");
const addInterestBtn = document.getElementById("addInterestBtn");
const lifeNoteInput = document.getElementById("lifeNoteInput");
const addLifeNoteBtn = document.getElementById("addLifeNoteBtn");
const examCatalogSelect = document.getElementById("examCatalogSelect");
const customExamNameInput = document.getElementById("customExamNameInput");
const examDateInput = document.getElementById("examDateInput");
const examSubjectsInput = document.getElementById("examSubjectsInput");
const examPortionInput = document.getElementById("examPortionInput");
const addExamBtn = document.getElementById("addExamBtn");
const examManager = document.getElementById("examManager");
const syllabusTitleInput = document.getElementById("syllabusTitleInput");
const syllabusTextInput = document.getElementById("syllabusTextInput");
const syllabusFileInput = document.getElementById("syllabusFileInput");
const uploadSyllabusBtn = document.getElementById("uploadSyllabusBtn");
const syllabusStatus = document.getElementById("syllabusStatus");
const syllabusManager = document.getElementById("syllabusManager");
const voiceChatMode = document.getElementById("voiceChatMode");
const nightModeToggle = document.getElementById("nightModeToggle");
const highContrastMode = document.getElementById("highContrastMode");
const largeTextMode = document.getElementById("largeTextMode");
const reducedMotionMode = document.getElementById("reducedMotionMode");
const readingComfortMode = document.getElementById("readingComfortMode");
const chunkedReplyMode = document.getElementById("chunkedReplyMode");
const responsePacingSelect = document.getElementById("responsePacingSelect");
const autoCaptionMode = document.getElementById("autoCaptionMode");
const tutorCaptionText = document.getElementById("tutorCaptionText");
const autoSpeakReplies = document.getElementById("autoSpeakReplies");
const speakLastReplyBtn = document.getElementById("speakLastReplyBtn");
const tutorVoiceInlineToggleBtn = document.getElementById("tutorVoiceInlineToggleBtn");
const pauseVoiceBtn = document.getElementById("pauseVoiceBtn");
const resumeVoiceBtn = document.getElementById("resumeVoiceBtn");
const stopVoiceBtn = document.getElementById("stopVoiceBtn");
const showTextExplanation = document.getElementById("showTextExplanation");
const showVideoExplanation = document.getElementById("showVideoExplanation");
const showVisualExplanation = document.getElementById("showVisualExplanation");
const showLeagueToggle = document.getElementById("showLeagueToggle");
const languageSelect = document.getElementById("languageSelect");
const tutorLanguageChip = document.getElementById("tutorLanguageChip");
const tutorLanguageDropdown = document.getElementById("tutorLanguageDropdown");
const tutorLanguageSelector = document.getElementById("tutor-language-selector");
const hinglishToggle = document.getElementById("hinglish-toggle");
const tabManager = document.getElementById("tabManager");
const tabBar = document.getElementById("tabBar");
const authHeroTitle = document.getElementById("authHeroTitle");
const authHeroQuote = document.getElementById("authHeroQuote");
const authHeroText = document.getElementById("authHeroText");
const authHeroBadges = document.getElementById("authHeroBadges");
const authHeroVideoPlayer = document.getElementById("authHeroVideoPlayer");
const authHeroVideoTitle = document.getElementById("authHeroVideoTitle");
const authHeroVideoMeta = document.getElementById("authHeroVideoMeta");
const authHeroVideoSummary = document.getElementById("authHeroVideoSummary");
const authHeroVideoTag = document.getElementById("authHeroVideoTag");
const authHeroVideoToggle = document.getElementById("authHeroVideoToggle");
const authCardKicker = document.getElementById("authCardKicker");
const introScreen = document.getElementById("introScreen");
const introTitle = document.getElementById("introTitle");
const introQuote = document.getElementById("introQuote");
const introText = document.getElementById("introText");
const introHint = document.getElementById("introHint");
const introVideoPlayer = document.getElementById("introVideoPlayer");
const introVideoTitle = document.getElementById("introVideoTitle");
const introVideoMeta = document.getElementById("introVideoMeta");
const introVideoSummary = document.getElementById("introVideoSummary");
const introVideoTag = document.getElementById("introVideoTag");
const introVideoToggle = document.getElementById("introVideoToggle");
const introContinueBtn = document.getElementById("introContinueBtn");
const introSoundBtn = document.getElementById("introSoundBtn");
const studioPaneButtons = Array.from(document.querySelectorAll(".studio-pane-button"));
const studioPanes = Array.from(document.querySelectorAll(".studio-pane"));
const fullscreenStudioBtn = document.getElementById("fullscreenStudioBtn");
const APP_CONFIG = window.APP_CONFIG || {};

let tabButtons = [];
let tabPanels = [];
let activeProfile = null;
let activeUser = null;
  let authSession = null;
  let avatarPresets = [];
  let activeAvatar = null;
  let avatarRenderer = null;
  let avatarConfigCache = null;
  let avatarStageInitPromise = null;
  let activeTutorBrain = null;
  let lastTutorReply = "";
  let lastTutorReplyText = "";
let lastTutorQuestion = "";
let lastVideoAnswerBrief = null;
let lastRepliesByMode = { tutor: "", guide: "", lounge: "", practice: "", last_minute: "", tips: "" };
let activeTutorNarration = null;
let activeSpeechUtterance = null;
let tutorReplyCheckpoints = { tutor: null, guide: null, lounge: null, practice: null, last_minute: null, tips: null };
let activeTutorVideoJobId = "";
let activeTutorVideoPollInterval = null;
let browserVoices = [];
window.astraCurrentTopic = window.astraCurrentTopic || { topic: null, subject: null, source: null };
let currentVideoTutorWeek = [];
let currentVideoTutorPlanStatus = [];
let currentRequestedVideos = [];
let activeVideoTutorBrief = null;
let activeVideoTutorRequest = null;
let videoSearchBound = false;
let activeVideoSubjectTab = "physics";
let activeVideoSearchQuery = "";
let activeVideoSubjectQuery = "";
let videoSubjectTabButtons = [];
const dismissedVideoSuggestionTopics = new Set();
const LoungeSpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition || null;
const LEGACY_TUTOR_ROOM_KEY = "tutor" + "room";
let loungeVoiceRecognition = null;
let loungeVoiceDraft = "";
let loungeVoicePrefix = "";
let loungeVoiceActive = false;
let currentLanguage = normalizeLanguageSelection(APP_CONFIG.default_language || "english");
window.astraLanguage = currentLanguage;
let currentTheme = "midnight";
let currentBackground = "glow";
let isSidebarCollapsed = false;
let leagueTabVisible = localStorage.getItem("alt_show_league_tab") !== "0";
let activeStudioPane = "threeConceptPanel";
let activeSummaryText = "";
let walkthroughContext = "signup";
let walkthroughStepIndex = 0;
let walkthroughAnswers = {};
let walkthroughProfileSnapshot = null;
let walkthroughParticleFrame = null;
let walkthroughParticleNodes = [];
let walkthroughTransitionTimer = null;
const DEFAULT_TAB_ORDER = Array.isArray(APP_CONFIG.default_tab_order) && APP_CONFIG.default_tab_order.length
  ? APP_CONFIG.default_tab_order.filter((key) => key !== LEGACY_TUTOR_ROOM_KEY && key !== "progress")
  : ["overview", "tutor", "videotutor", "formulas", "practice", "tips", "lastminute", "mocktest", "weekly", "lounge", "network", "league", "personalize", "guide", "assist"];
let currentTabOrder = [...DEFAULT_TAB_ORDER];
let isSending = false;
let loungeTimerInterval = null;
let loungeTimerEndTime = null;
let examCatalog = [];
let activeTutorVideo = null;
let videoLibrarySnapshot = null;
let authHeroVideoSnapshot = null;
let introVideoSnapshot = null;
let introVideoMode = "signin";
let activeTutorCheckpoint = null;
let activeVideoTimer = null;
let activeLessonNarration = null;
let activeVideoExplanation = null;
let tutorStageFocusTimer = null;
let pendingDoubtImage = null;
let lastPracticeMode = "general";
let activeConceptAnimation = null;
let activeTutorConversationId = null;
let journeyPlanSnapshot = null;
let journeyWeeklySnapshot = null;
let todaysFocusSnapshot = null;
let latestProgressSnapshot = null;
let latestPhaseStatus = null;
let latestEngagementSnapshot = null;
let journeyTimerInterval = null;
let journeyTimerStartedAt = null;
let activeJourneySession = null;
let chapterMasterySnapshot = null;
let chapterAnalyticsSnapshot = null;
let chapterRevisionSnapshot = null;
let selectedChapterSnapshot = null;
let formulasDatabase = null;
let formulaChapters = [];
let selectedFormulaChapterKey = "";
let activeFormulaSubjects = new Set(["physics", "chemistry", "mathematics"]);
let formulaWeakTopicTerms = new Set();
let formulaWeakLoadedFor = "";
let activeChapterSession = null;
let activeChapterSubtopic = null;
let activeChapterTest = null;
let activeChapterTestStartedAt = null;
let activeChapterTestInterval = null;
let activeChapterBreakInterval = null;
let activeChapterBreakEndAt = null;
let activeChapterCompletionMode = null;
let activeChapterTestAnswers = [];
let activeChapterResumeSummary = null;
let chapterResumeLoadedFor = "";
let chapterResumeDismissedFor = "";
let chapterResumeBannerDismissedFor = "";
let tutorConversationSearch = "";
let tutorConversationSnapshot = [];
let deletedTutorConversationSnapshot = [];
let activeTutorMode = localStorage.getItem("alt_tutor_mode") || "calm";
let activeLoungeConversationId = null;
let loungeConversationSearch = "";
let loungeConversationSnapshot = [];
let deletedLoungeConversationSnapshot = [];
let selectedTutorTraits = [];
let activeGroupSession = null;
let activeMockTest = null;
let activeMockIndex = 0;
let activeMockAnswers = [];
let activeMockStartAt = null;
let activeMockTimerInterval = null;
let activeMockDurationMinutes = 60;
let activeMockQuestionTimes = {};
let activeMockQuestionStartedAt = null;
let mockCatalogue = [];
let selectedMockTestId = "";
let lastNonMockTabId = "practiceTab";

const TUTOR_PERSONALITY_TRAITS = [
  { key: "patient", label: "Patient" },
  { key: "strict", label: "Strict" },
  { key: "friendly", label: "Friendly" },
  { key: "motivational", label: "Motivational" },
  { key: "witty", label: "Witty" },
  { key: "structured", label: "Structured" },
  { key: "calm", label: "Calm" },
  { key: "energetic", label: "Energetic" },
  { key: "exam-focused", label: "Exam-focused" },
];
let splashDismissed = false;

const ASTRA_PIXEL_PATTERNS = {
  A: ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
  S: ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
  T: ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
  R: ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
};

const LEAGUE_ORDER = [
  "Bronze 1",
  "Bronze 2",
  "Bronze 3",
  "Silver 1",
  "Silver 2",
  "Silver 3",
  "Gold 1",
  "Gold 2",
  "Gold 3",
  "Platinum 1",
  "Platinum 2",
  "Platinum 3",
  "Diamond 1",
  "Diamond 2",
  "Diamond 3",
  "Champion",
];

function safeJsonParse(rawValue, fallback) {
  try {
    return JSON.parse(rawValue);
  } catch (error) {
    return fallback;
  }
}

function getLanguagePrefix(language) {
  const normalized = String(language || "English").toLowerCase();
  const map = {
    english: "en",
    hindi: "hi",
    tamil: "ta",
    telugu: "te",
    kannada: "kn",
    malayalam: "ml",
    marathi: "mr",
    gujarati: "gu",
    bengali: "bn",
    punjabi: "pa",
    urdu: "ur",
    spanish: "es",
    french: "fr",
  };
  return map[normalized] || "en";
}

function normalizeExamName(value) {
  return String(value || "").trim();
}

function getProfileExamEntries(profile = activeProfile) {
  const entries = Array.isArray(profile && profile.exams) ? profile.exams : [];
  return entries
    .map((exam) => normalizeExamName(exam && exam.name))
    .filter(Boolean);
}

function getPrimaryExamName(profile = activeProfile) {
  const examEntries = getProfileExamEntries(profile);
  if (examEntries.length) {
    return examEntries[0];
  }
  const profileExam = normalizeExamName(profile && profile.exam);
  if (profileExam) {
    return profileExam;
  }
  return normalizeExamName(APP_CONFIG.default_exam) || "your exam";
}

function getExamFamilyLabel(examName) {
  const normalized = normalizeExamName(examName).toUpperCase();
  if (!normalized) {
    return "JEE";
  }
  if (normalized.includes("JEE")) {
    return "JEE";
  }
  return "JEE";
}

function getActiveExamLabel(profile = activeProfile) {
  return getExamFamilyLabel(getPrimaryExamName(profile));
}

function getActiveExamListLabel(profile = activeProfile) {
  const examEntries = getProfileExamEntries(profile);
  if (examEntries.length) {
    return examEntries.join(", ");
  }
  return normalizeExamName(APP_CONFIG.default_exam) || "your exam";
}

function updateExamBrandCopy(profile = activeProfile, mode = "signin") {
  const examLabel = getActiveExamLabel(profile);
  const isGenericExam = examLabel === "your exam";

  if (authHeroTitle) {
    authHeroTitle.textContent = isGenericExam
      ? "Study for your exam with an AI teacher that feels bright, human, and easy to come back to."
      : `Study for ${examLabel} with an AI teacher that feels bright, human, and easy to come back to.`;
  }
  if (authHeroQuote) {
    authHeroQuote.textContent = isGenericExam
      ? "Your journey starts here with Astra."
      : `Your ${examLabel} journey starts here with Astra.`;
  }
  if (authHeroText) {
    authHeroText.textContent = isGenericExam
      ? "Personalized tutoring, adaptive planning, revision support, practice drills, and a warm AI guide that helps students feel comfortable before jumping into serious prep."
      : `Personalized ${examLabel} tutoring, adaptive planning, revision support, practice drills, and a warm AI guide that helps students feel comfortable before jumping into serious prep.`;
  }
  if (authCardKicker) {
    authCardKicker.textContent = isGenericExam ? "Learning Studio Access" : `${examLabel} Learning Studio Access`;
  }
  if (authHeroBadges) {
    const badges = Array.from(authHeroBadges.querySelectorAll("span"));
    const badgeValues = isGenericExam
      ? ["Personalized", "Accessible", "Custom Themes", "Personal Tutor"]
      : [examLabel, "Adaptive", "Custom Themes", "Personal Tutor"];
    badges.forEach((badge, index) => {
      if (badgeValues[index]) {
        badge.textContent = badgeValues[index];
      }
    });
  }
  if (authTitle) {
    authTitle.textContent = mode === "signup"
      ? (isGenericExam
        ? "Create your account for the learning studio"
        : `Create your account for the ${examLabel} learning studio`)
      : (isGenericExam
        ? "Sign in to the learning studio"
        : `Sign in to the ${examLabel} learning studio`);
  }
  if (authSubtitle) {
    authSubtitle.textContent = mode === "signup"
      ? "Use the sign-up form below to create a fresh account and linked student profile."
      : (isGenericExam
        ? "Sign in with your account to open your personal learning studio."
        : `Sign in with your account to open your personal ${examLabel} learning studio.`);
  }
}

const TAB_CONFIG = {
  overview: { buttonTab: "overviewTab", label: "Overview" },
  tutor: { buttonTab: "tutorTab", label: "Tutor" },
  videotutor: { buttonTab: "videoTutorTab", label: "Video Tutor" },
  formulas: { buttonTab: "formulasTab", label: "Formulas" },
  practice: { buttonTab: "practiceTab", label: "Practice" },
  mocktest: { buttonTab: "mockTestTab", label: "Mock Test" },
  lastminute: { buttonTab: "lastMinuteTab", label: "Last Minute" },
  tips: { buttonTab: "tipsTab", label: "Tips" },
  weekly: { buttonTab: "weeklyTab", label: "Plan" },
  lounge: { buttonTab: "loungeTab", label: "Lounge" },
  network: { buttonTab: "networkTab", label: "Study groups" },
  league: { buttonTab: "leagueTab", label: "League" },
  personalize: { buttonTab: "personalizeTab", label: "Personalize" },
  guide: { buttonTab: "guideTab", label: "Guide" },
  assist: { buttonTab: "assistTab", label: "Assist" },
};

const MOTIVATIONAL_QUOTES = [
  "Small wins compound into serious exam momentum.",
  "Stay steady today and your future self will thank you.",
  "Master the next step, then the next one gets easier.",
  "Consistency is a quiet superpower.",
  "Progress becomes confidence when you keep showing up.",
  "Astra is here to help you keep moving forward.",
];

let motivationStories = [];
let activeMotivationStoryIndex = 0;
let motivationStoryOpen = false;
let activeHomeSubtab = "overview";
let activePlanSubtab = "today";
let pendingPlanSubtab = "";
let homeSubtabButtons = [];
let homeSubtabPanels = [];
let planSubtabButtons = [];
let planSubtabPanels = [];
let sectionNavButtons = [];
let activeSectionGroup = "home";
let astraStatusTimer = null;
let sessionActivityLog = [];
let sessionCheckpointStats = {
  answered: 0,
  average: 0,
  confidence: "new",
  topic: "",
};
let dailyBriefingLoadedDate = "";
let dailyBriefingDismissedDate = "";
let toastTimer = null;
if (sessionActivityToggleBtn && sessionActivityPanel && sessionActivityPanel.classList.contains("hidden")) {
  sessionActivityToggleBtn.textContent = "Session log >";
}

function refreshTabCollections() {
  tabButtons = Array.from(document.querySelectorAll(".tab-button"));
  tabPanels = Array.from(document.querySelectorAll(".tab-panel"));
  sectionNavButtons = Array.from(document.querySelectorAll(".section-nav-button"));
  homeSubtabButtons = Array.from(document.querySelectorAll("[data-home-subtab]"));
  homeSubtabPanels = Array.from(document.querySelectorAll("[data-home-subtab-panel]"));
  planSubtabButtons = Array.from(document.querySelectorAll("[data-plan-subtab]"));
  planSubtabPanels = Array.from(document.querySelectorAll("[data-plan-subtab-panel]"));
  videoSubjectTabButtons = Array.from(document.querySelectorAll("[data-video-subject-tab]"));
  homeSubtabButtons.forEach((button) => {
    if (button.dataset.homeSubtabBound === "1") {
      return;
    }
    button.dataset.homeSubtabBound = "1";
    button.addEventListener("click", () => {
      if (document.querySelector("#overviewTab") && !document.querySelector("#overviewTab").classList.contains("active")) {
        setActiveTab("overviewTab");
      }
      setHomeSubtab(button.dataset.homeSubtab);
    });
  });
  planSubtabButtons.forEach((button) => {
    if (button.dataset.planSubtabBound === "1") {
      return;
    }
    button.dataset.planSubtabBound = "1";
    button.addEventListener("click", () => {
      if (document.querySelector("#weeklyTab") && !document.querySelector("#weeklyTab").classList.contains("active")) {
        pendingPlanSubtab = button.dataset.planSubtab || "today";
        setActiveTab("weeklyTab");
        return;
      }
      setPlanSubtab(button.dataset.planSubtab);
    });
  });
  videoSubjectTabButtons.forEach((button) => {
    if (button.dataset.videoSubjectTabBound === "1") {
      return;
    }
    button.dataset.videoSubjectTabBound = "1";
    button.addEventListener("click", () => {
      switchVideoSubjectTab(button.dataset.videoSubjectTab || "physics");
    });
  });
  sectionNavButtons.forEach((button) => {
    if (button.dataset.sectionBound === "1") {
      return;
    }
    button.dataset.sectionBound = "1";
    button.addEventListener("click", () => {
      setActiveSectionGroup(button.dataset.sectionGroup);
    });
  });
}

function keepTabPanelNearTop(tabId) {
  const panel = document.getElementById(tabId);
  const statusBar = document.getElementById("astra-status-bar");
  if (!panel || !statusBar || !statusBar.parentElement) {
    return;
  }
  if (statusBar.nextElementSibling !== panel) {
    statusBar.insertAdjacentElement("afterend", panel);
  }
}

function keepPlanPanelNearTop() {
  keepTabPanelNearTop("weeklyTab");
}

function scrollActivePanelToTop(tabId) {
  const panel = document.getElementById(tabId);
  if (!panel || !panel.classList.contains("active")) {
    return;
  }
  window.setTimeout(() => {
    const target = document.getElementById("tabBar") || panel;
    if (target && typeof target.scrollIntoView === "function") {
      target.scrollIntoView({ block: "start" });
    }
  }, 0);
}

function scrollPlanPanelToTop() {
  scrollActivePanelToTop("weeklyTab");
}

function setActiveSectionGroup(section = "home", { skipTabSwitch = false } = {}) {
  const nextSection = ["home", "learn", "plan", "connect", "settings"].includes(String(section || "").trim())
    ? String(section || "").trim()
    : "home";
  activeSectionGroup = nextSection;
  sectionNavButtons.forEach((button) => {
    const isActive = button.dataset.sectionGroup === activeSectionGroup;
    button.classList.toggle("active", isActive);
    button.setAttribute("aria-selected", String(isActive));
  });
  document.querySelectorAll(".nav-hub[data-section-group]").forEach((hub) => {
    const isActive = hub.dataset.sectionGroup === activeSectionGroup;
    hub.classList.toggle("hidden", !isActive);
    hub.hidden = !isActive;
    hub.setAttribute("aria-hidden", String(!isActive));
  });
  if (!skipTabSwitch) {
    const defaultTabs = {
      home: "overviewTab",
      learn: "tutorTab",
      plan: "weeklyTab",
      connect: "loungeTab",
      settings: "personalizeTab",
    };
    const defaultTab = defaultTabs[activeSectionGroup] || "overviewTab";
    setActiveTab(defaultTab);
  }
}

function setHomeSubtab(subtab = "overview") {
  const nextSubtab = ["overview", "motivation", "personality"].includes(String(subtab || "").trim())
    ? String(subtab || "").trim()
    : "overview";
  activeHomeSubtab = nextSubtab;
  homeSubtabButtons.forEach((button) => {
    const isActive = button.dataset.homeSubtab === activeHomeSubtab;
    button.classList.toggle("active", isActive);
    button.setAttribute("aria-selected", String(isActive));
  });
  homeSubtabPanels.forEach((panel) => {
    const isActive = panel.dataset.homeSubtabPanel === activeHomeSubtab;
    panel.classList.toggle("hidden", !isActive);
    panel.classList.toggle("active", isActive);
    panel.hidden = !isActive;
    panel.setAttribute("aria-hidden", String(!isActive));
  });
  if (activeHomeSubtab === "personality") {
    renderHomeTutorPersonalityGrid();
  } else if (activeHomeSubtab === "motivation") {
    renderDailyMotivation(activeProfile?.name || "");
    if (!motivationStories.length) {
      void fetchMotivationSection();
    } else {
      renderMotivationStory(activeMotivationStoryIndex);
    }
  }
  updateOverviewCommandCenter();
  scrollActivePanelToTop("overviewTab");
}

function setPlanSubtab(subtab = "today") {
  keepPlanPanelNearTop();
  const nextSubtab = ["today", "thisweek", "journey", "strategy", "progress"].includes(String(subtab || "").trim())
    ? String(subtab || "").trim()
    : "today";
  activePlanSubtab = nextSubtab;
  planSubtabButtons.forEach((button) => {
    const isActive = button.dataset.planSubtab === activePlanSubtab;
    button.classList.toggle("active", isActive);
    button.setAttribute("aria-selected", String(isActive));
  });
  planSubtabPanels.forEach((panel) => {
    const isActive = panel.dataset.planSubtabPanel === activePlanSubtab;
    panel.classList.toggle("active", isActive);
    panel.classList.remove("hidden");
    panel.style.display = isActive ? "block" : "none";
    panel.setAttribute("aria-hidden", String(!isActive));
  });
  if (!activeProfile) {
    scrollPlanPanelToTop();
    return;
  }
  if (activePlanSubtab === "today") {
    window.setTimeout(() => {
      void refreshTodayPhaseAndBacklog();
    }, 0);
  } else if (activePlanSubtab === "progress") {
    window.setTimeout(() => {
      fetchProgress(activeProfile.name);
    }, 0);
  } else if (activePlanSubtab === "thisweek") {
    window.setTimeout(() => {
      refreshWeeklyPlan();
    }, 0);
  } else if (activePlanSubtab === "journey") {
    window.setTimeout(() => {
      refreshJourneyDashboard();
      refreshActiveChapterSession();
      fetchProgress(activeProfile.name);
    }, 0);
  } else if (activePlanSubtab === "strategy") {
    window.setTimeout(() => {
      refreshWeeklyPlan();
      refreshJourneyDashboard();
      refreshActiveChapterSession();
    }, 0);
  }
  scrollPlanPanelToTop();
}

function openPlanSubtab(subtab = "today") {
  pendingPlanSubtab = subtab;
  setActiveTab("weeklyTab");
}

function setAstraStatus(message, type = "idle", autoClear = false) {
  if (!astraStatusBar) {
    return;
  }
  const normalized = String(message || "").trim();
  astraStatusBar.textContent = normalized || "Astra is ready.";
  astraStatusBar.dataset.state = type || "idle";
  astraStatusBar.classList.remove("hide-status");
  astraStatusBar.classList.add("show-status");
  if (astraStatusTimer) {
    window.clearTimeout(astraStatusTimer);
    astraStatusTimer = null;
  }
  if (autoClear && type !== "idle") {
    astraStatusTimer = window.setTimeout(() => {
      if (astraStatusBar) {
        astraStatusBar.classList.add("hide-status");
        astraStatusBar.textContent = "Astra is ready.";
        astraStatusBar.dataset.state = "idle";
      }
    }, 4000);
  }
}

function showToast(message, type = "success") {
  const existing = document.querySelector(".astra-toast");
  if (existing) {
    existing.remove();
  }
  const toast = document.createElement("div");
  toast.className = `astra-toast ${type || "success"}`;
  toast.textContent = String(message || "").trim();
  document.body.appendChild(toast);
  if (toastTimer) {
    window.clearTimeout(toastTimer);
  }
  toastTimer = window.setTimeout(() => {
    toast.classList.add("hide-toast");
    window.setTimeout(() => toast.remove(), 220);
  }, 4000);
}
function showLPToast(amount, reason) {
  const value = Number(amount || 0);
  if (!value) {
    return;
  }
  showToast(`+${value} LP - ${reason || "League points earned"}`, "success");
}

function showTierPromotion(oldTier, newTier) {
  if (!oldTier || !newTier || oldTier === newTier) {
    return;
  }
  const modal = document.createElement("div");
  modal.className = "phase-transition-modal tier-promotion-modal";
  modal.innerHTML = `
    <div class="phase-transition-card">
      <p class="eyebrow">League Promotion</p>
      <h3>Tier Up!</h3>
      <p>${escapeHtml(oldTier)} -> ${escapeHtml(newTier)}</p>
      <button type="button">Nice</button>
    </div>
  `;
  const close = () => modal.remove();
  modal.querySelector("button").addEventListener("click", close);
  modal.addEventListener("click", (event) => {
    if (event.target === modal) {
      close();
    }
  });
  document.body.appendChild(modal);
  window.setTimeout(close, 5000);
}

function handleLPAwards(awards) {
  const items = Array.isArray(awards) ? awards : [];
  items.forEach((award) => {
    showLPToast(award.amount || award.points, award.reason);
  });
}

async function refreshEngagementAfterLPAward(awards) {
  handleLPAwards(awards);
  if (activeProfile) {
    try {
      await fetchEngagement(activeProfile.name);
    } catch (error) {
      console.warn("Could not refresh engagement after LP award:", error);
    }
  }
}

function showKnowledgeBaseTag(text, visible = false) {
  if (!kbStatusTag) {
    return;
  }
  const content = String(text || "").trim();
  kbStatusTag.textContent = content;
  kbStatusTag.classList.toggle("hidden", !visible || !content);
}

function getActiveTutorFocus() {
  const focus = todaysFocusSnapshot && (todaysFocusSnapshot.primary || todaysFocusSnapshot.morning)
    ? (todaysFocusSnapshot.primary || todaysFocusSnapshot.morning)
    : {};
  const chapterFocus = activeChapterSubtopic || {};
  return {
    topic: chapterFocus.subtopic_name || chapterFocus.chapter_name || focus.topic || "today's topic",
    subject: chapterFocus.subject || focus.subject || (activeProfile && activeProfile.exams && activeProfile.exams[0] && activeProfile.exams[0].subjects && activeProfile.exams[0].subjects[0]) || "physics",
    unit: chapterFocus.chapter_name || focus.unit || focus.unit_name || "",
    isChapter: Boolean(chapterFocus.subtopic_id || activeChapterSession),
  };
}

function updateSessionCheckpointStats({ topic, score, confidence } = {}) {
  const normalizedScore = Number(score || 0);
  sessionCheckpointStats.topic = topic || sessionCheckpointStats.topic || "";
  sessionCheckpointStats.answered = Math.max(0, Number(sessionCheckpointStats.answered || 0)) + 1;
  const previousAverage = Number(sessionCheckpointStats.average || 0);
  sessionCheckpointStats.average = Math.round((previousAverage * (sessionCheckpointStats.answered - 1) + normalizedScore) / sessionCheckpointStats.answered);
  sessionCheckpointStats.confidence = confidence || sessionCheckpointStats.confidence || "new";
  renderSessionStats(sessionCheckpointStats.topic, sessionCheckpointStats.confidence, sessionCheckpointStats.average);
}

function logSessionActivity(message) {
  const text = String(message || "").trim();
  if (!text) {
    return;
  }
  const stamp = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  sessionActivityLog.unshift({ stamp, text });
  sessionActivityLog = sessionActivityLog.slice(0, 12);
  renderSessionActivity();
}

function renderDailyBriefingCard(briefing = null) {
  if (!dailyBriefingCard || !dailyBriefingText) {
    return;
  }
  if (!briefing) {
    dailyBriefingText.textContent = "Your briefing will appear here.";
    dailyBriefingCard.classList.add("hidden");
    return;
  }
  const parts = [briefing.greeting, briefing.accomplish, briefing.motivation].filter(Boolean);
  dailyBriefingText.textContent = parts.join(" ").trim();
  dailyBriefingCard.classList.remove("hidden");
}

function focusTutorComposerWithPrompt(prompt = "") {
  setActiveTab("tutorTab");
  if (messageInput) {
    messageInput.value = String(prompt || "");
    window.setTimeout(() => messageInput.focus(), 0);
  }
}

function startTodaySessionFromHome() {
  if (activeJourneySession || (todaysFocusSnapshot && (todaysFocusSnapshot.primary || todaysFocusSnapshot.morning))) {
    void startJourneySession();
    return;
  }
  setActiveTab("weeklyTab");
}

function renderSessionActivity() {
  if (!sessionActivityList) {
    return;
  }
  sessionActivityList.innerHTML = "";
  if (!sessionActivityLog.length) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = "Session events will appear here as Astra teaches.";
    sessionActivityList.appendChild(empty);
    return;
  }
  sessionActivityLog.forEach((entry) => {
    const row = document.createElement("div");
    row.className = "session-activity-item";
    row.innerHTML = `<span class="session-activity-stamp">${entry.stamp}</span><span>${escapeHtml(entry.text)}</span>`;
    sessionActivityList.appendChild(row);
  });
}

function renderSessionStats(topic = "", confidence = "new", score = 0) {
  sessionCheckpointStats.topic = topic || sessionCheckpointStats.topic || "";
  sessionCheckpointStats.confidence = confidence || sessionCheckpointStats.confidence || "new";
  if (Number.isFinite(Number(score))) {
    sessionCheckpointStats.average = Math.max(0, Math.min(100, Number(score || 0)));
  }
  if (sessionStatsTopic) {
    sessionStatsTopic.textContent = `Current topic: ${sessionCheckpointStats.topic || "-"}`;
  }
  if (sessionStatsConfidence) {
    sessionStatsConfidence.textContent = sessionCheckpointStats.confidence || "new";
  }
  if (sessionStatsCount) {
    sessionStatsCount.textContent = String(Math.max(0, sessionCheckpointStats.answered || 0));
  }
  if (sessionStatsAverage) {
    sessionStatsAverage.textContent = `${Math.max(0, Math.min(100, Number(sessionCheckpointStats.average || 0)))}%`;
  }
  if (sessionStatsStreak) {
    sessionStatsStreak.textContent = activeProfile && activeProfile.streak_days ? `${activeProfile.streak_days} days` : "0";
  }
  renderTutorSideSessionSummary();
}

function getProgressStatusPhrase(status) {
  const value = String(status || "").trim().toLowerCase();
  if (value === "done") return "solid";
  if (value === "revise") return "needs another look";
  if (value === "pending") return "not started yet";
  return "building";
}

function getLatestProgressItem(snapshot) {
  const items = Array.isArray(snapshot && snapshot.items) ? snapshot.items : [];
  return [...items].sort((a, b) => String(b.updated_at || "").localeCompare(String(a.updated_at || "")))[0] || null;
}

function updateOverviewCommandCenter() {
  const focus = todaysFocusSnapshot && (todaysFocusSnapshot.primary || todaysFocusSnapshot.morning) ? (todaysFocusSnapshot.primary || todaysFocusSnapshot.morning) : {};
  if (overviewCommandTopic) {
    overviewCommandTopic.textContent = focus.topic || "Today's topic";
  }
  if (overviewCommandBadge) {
    overviewCommandBadge.textContent = focus.session_type ? String(focus.session_type).replace(/_/g, " ") : "Learning";
  }
  if (overviewCommandReason) {
    overviewCommandReason.textContent = focus.daily_goal || "Your next step will appear here.";
  }
  if (overviewCommandSubject) {
    overviewCommandSubject.textContent = focus.subject || "-";
  }
  if (overviewCommandTime) {
    overviewCommandTime.textContent = focus.duration_minutes ? `${focus.duration_minutes} min` : "-";
  }
  if (overviewCommandWhy) {
    overviewCommandWhy.textContent = focus.weightage ? `${focus.weightage}% of JEE Main` : "JEE focus";
  }
  const mastery = chapterMasterySnapshot || {};
  const covered = mastery.covered_count || 0;
  const total = mastery.total_count || 0;
  if (overviewMetricCovered) {
    overviewMetricCovered.textContent = `${covered}/${total}`;
  }
  if (overviewMetricAverage) {
    overviewMetricAverage.textContent = `${Math.round(mastery.average_score || 0)}%`;
  }
  if (overviewMetricStreak) {
    overviewMetricStreak.textContent = `${(activeProfile && activeProfile.streak_days) || 0} days`;
  }

  const progress = latestProgressSnapshot || {};
  const counts = progress.counts || {};
  const latestItem = getLatestProgressItem(progress);
  const fallbackTopic = focus.topic ? { topic: focus.topic, subject: focus.subject || "", status: "pending" } : null;
  const displayItem = latestItem || fallbackTopic;
  if (overviewLastTopic) {
    overviewLastTopic.textContent = displayItem && displayItem.topic
      ? `${displayItem.topic}${displayItem.subject ? ` - ${displayItem.subject}` : ""}`
      : "No recent topic yet";
  }
  if (overviewLastTopicStatus) {
    overviewLastTopicStatus.textContent = displayItem
      ? `Status: ${getProgressStatusPhrase(displayItem.status)}.`
      : "Start a session or save progress to build this view.";
  }
  if (overviewProgressBadge) {
    overviewProgressBadge.textContent = counts.total ? `${counts.completion_rate || 0}% complete` : "Starting";
  }
  if (overviewDoneCount) overviewDoneCount.textContent = counts.done || 0;
  if (overviewReviseCount) overviewReviseCount.textContent = counts.revise || 0;
  if (overviewPendingCount) overviewPendingCount.textContent = counts.pending || 0;
  if (overviewNextStep) {
    const momentum = progress.topic_momentum || {};
    overviewNextStep.textContent = momentum.next_focus
      || (counts.pending ? "Clear one pending topic before adding more." : "Keep a light revision loop going.");
  }

  if (astraStatusBar) {
    setAstraStatus(
      focus.topic
        ? `Astra is ready. Today's focus: ${focus.topic} - ${focus.subject || "study"}`
        : "Astra is ready. Today's focus: -",
      "idle"
    );
  }
}

function updateContextPanel() {
  return;
}

function renderTutorSmartPrompts() {
  if (!tutorSmartPromptChips) {
    return;
  }
  const focus = todaysFocusSnapshot && (todaysFocusSnapshot.primary || todaysFocusSnapshot.morning) ? (todaysFocusSnapshot.primary || todaysFocusSnapshot.morning) : {};
  const chapterActive = isChapterCheckpointActive();
  const prompts = chapterActive
    ? [
        `I didn't understand ${activeChapterSubtopic.subtopic_name || "this subtopic"}`,
        "Give me another example",
        "Make this simpler",
        "What's the JEE trap here?",
      ]
    : [
        `Explain ${focus.topic || "today's topic"} from the beginning`,
        `What is the most important formula in ${focus.topic || "this topic"}?`,
        `Give me a JEE question on ${focus.topic || "this topic"}`,
      ];
  if (tutorSmartPromptLine) {
    tutorSmartPromptLine.textContent = chapterActive
      ? `Focus now: ${activeChapterSubtopic.subtopic_name || "this subtopic"}`
      : `Focus now: ${focus.topic || "today's topic"}`;
  }
  tutorSmartPromptChips.innerHTML = "";
  prompts.forEach((prompt) => {
    const chip = document.createElement("button");
    chip.type = "button";
    chip.className = "soft-chip tutor-smart-chip";
    chip.textContent = prompt;
    chip.addEventListener("click", () => {
      if (messageInput) {
        messageInput.value = prompt;
        messageInput.focus();
        updateTutorSuggestedPromptsVisibility();
      }
    });
    tutorSmartPromptChips.appendChild(chip);
  });
}

function _setTutorTopToggle(button, on, onLabel, offLabel) {
  if (!button) {
    return;
  }
  button.classList.toggle("active", !!on);
  button.textContent = on ? onLabel : offLabel;
}

function syncTutorControlStrip() {
  const voiceOn = !!(voiceChatMode && voiceChatMode.checked);
  const speakOn = !!(autoSpeakReplies && autoSpeakReplies.checked);
  const captionOn = !!(autoCaptionMode && autoCaptionMode.checked);
  const readingOn = !!(readingComfortMode && readingComfortMode.checked);
  const paceValue = (responsePacingSelect && responsePacingSelect.value) || "gentle";
  const levelValue = String((tutorLevelSelect && tutorLevelSelect.value) || "3");

  _setTutorTopToggle(document.getElementById("tutorVoiceToggleBtn"), voiceOn, "Voice on", "Voice off");
  _setTutorTopToggle(tutorVoiceInlineToggleBtn, voiceOn, "Voice on", "Voice off");
  _setTutorTopToggle(document.getElementById("tutorSpeakToggleBtn"), speakOn, "Speak on", "Speak off");
  _setTutorTopToggle(document.getElementById("tutorCaptionToggleBtn"), captionOn, "Captions on", "Captions off");
  _setTutorTopToggle(document.getElementById("tutorReadingToggleBtn"), readingOn, "Read on", "Read off");
  _setTutorTopToggle(document.getElementById("tutorPaceGentleBtn"), paceValue === "gentle", "Gentle", "Gentle");
  _setTutorTopToggle(document.getElementById("tutorPaceNormalBtn"), paceValue === "standard" || paceValue === "normal", "Normal", "Normal");
  _setTutorTopToggle(document.getElementById("tutorPaceFastBtn"), paceValue === "fast", "Fast", "Fast");
  const levelSelect = document.getElementById("tutorTopLevelSelect");
  if (levelSelect) {
    levelSelect.value = levelValue;
  }
}

function _buildTutorVoiceControlsMirror() {
  const card = document.createElement("div");
  card.className = "table-card compact-side-card";
  card.innerHTML = `
    <div class="card-header">
      <div>
        <p class="card-title">Voice controls</p>
        <p class="muted">All reply controls, mirrored in a compact panel.</p>
      </div>
    </div>
    <div class="voice-controls-grid" id="tutorVoiceControlsGrid"></div>
    <div class="voice-controls-grid">
      <button type="button" class="ghost-button" id="tutorVoiceSpeakLastSideBtn">Speak last reply</button>
      <button type="button" class="ghost-button" id="tutorVoicePauseSideBtn">Pause</button>
      <button type="button" class="ghost-button" id="tutorVoiceResumeSideBtn">Resume</button>
      <button type="button" class="ghost-button" id="tutorVoiceStopSideBtn">Stop</button>
    </div>
  `;
  const grid = card.querySelector("#tutorVoiceControlsGrid");
  const controls = [
    { id: "tutorVoiceOnSideBtn", label: "Voice on/off", getter: () => !!(voiceChatMode && voiceChatMode.checked), toggle: () => voiceChatMode && (voiceChatMode.checked = !voiceChatMode.checked) },
    { id: "tutorAutoSpeakSideBtn", label: "Auto-speak", getter: () => !!(autoSpeakReplies && autoSpeakReplies.checked), toggle: () => autoSpeakReplies && (autoSpeakReplies.checked = !autoSpeakReplies.checked) },
    { id: "tutorCaptionsSideBtn", label: "Captions", getter: () => !!(autoCaptionMode && autoCaptionMode.checked), toggle: () => autoCaptionMode && (autoCaptionMode.checked = !autoCaptionMode.checked) },
    { id: "tutorReadingSideBtn", label: "Reading comfort", getter: () => !!(readingComfortMode && readingComfortMode.checked), toggle: () => readingComfortMode && (readingComfortMode.checked = !readingComfortMode.checked) },
  ];
  controls.forEach((entry) => {
    const button = document.createElement("button");
    button.type = "button";
    button.id = entry.id;
    button.className = "ghost-button";
    const refresh = () => {
      button.textContent = `${entry.label}: ${entry.getter() ? "On" : "Off"}`;
      button.classList.toggle("active", entry.getter());
    };
    refresh();
    button.addEventListener("click", () => {
      entry.toggle();
      if (voiceChatMode) voiceChatMode.dispatchEvent(new Event("change", { bubbles: true }));
      if (autoSpeakReplies && entry.id === "tutorAutoSpeakSideBtn") autoSpeakReplies.dispatchEvent(new Event("change", { bubbles: true }));
      if (autoCaptionMode && entry.id === "tutorCaptionsSideBtn") autoCaptionMode.dispatchEvent(new Event("change", { bubbles: true }));
      if (readingComfortMode && entry.id === "tutorReadingSideBtn") readingComfortMode.dispatchEvent(new Event("change", { bubbles: true }));
      refresh();
      syncTutorControlStrip();
    });
    grid.appendChild(button);
  });

  const paceRow = document.createElement("div");
  paceRow.className = "voice-controls-grid";
  ["gentle", "standard", "fast"].forEach((pace) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "ghost-button";
    button.dataset.pace = pace;
    button.textContent = pace.charAt(0).toUpperCase() + pace.slice(1);
    button.addEventListener("click", () => {
      if (responsePacingSelect) {
        responsePacingSelect.value = pace;
        responsePacingSelect.dispatchEvent(new Event("change", { bubbles: true }));
      }
      syncTutorControlStrip();
    });
    paceRow.appendChild(button);
  });
  card.appendChild(paceRow);

  const levelRow = document.createElement("div");
  levelRow.className = "inline-form";
  levelRow.innerHTML = `
    <label class="muted" for="tutorVoiceLevelSelect">Tutor level</label>
    <select id="tutorVoiceLevelSelect">
      <option value="1">Level 1</option>
      <option value="2">Level 2</option>
      <option value="3" selected>Level 3</option>
      <option value="4">Level 4</option>
      <option value="5">Level 5</option>
    </select>
  `;
  const levelSelect = levelRow.querySelector("#tutorVoiceLevelSelect");
  if (levelSelect && tutorLevelSelect) {
    levelSelect.value = tutorLevelSelect.value || "3";
    levelSelect.addEventListener("change", () => {
      tutorLevelSelect.value = levelSelect.value;
      tutorLevelSelect.dispatchEvent(new Event("change", { bubbles: true }));
      syncTutorControlStrip();
    });
  }
  card.appendChild(levelRow);

  const speakLast = card.querySelector("#tutorVoiceSpeakLastSideBtn");
  if (speakLast) {
    speakLast.addEventListener("click", () => {
      if (lastTutorReply) {
        speakText(lastTutorReply);
      }
    });
  }
  const pauseBtn = card.querySelector("#tutorVoicePauseSideBtn");
  if (pauseBtn) {
    pauseBtn.addEventListener("click", () => pauseTutorNarration());
  }
  const resumeBtn = card.querySelector("#tutorVoiceResumeSideBtn");
  if (resumeBtn) {
    resumeBtn.addEventListener("click", () => resumeTutorNarration());
  }
  const stopBtn = card.querySelector("#tutorVoiceStopSideBtn");
  if (stopBtn) {
    stopBtn.addEventListener("click", () => interruptTutorOutput("tutor"));
  }
  return card;
}

function setTutorSidePanelTab(tab = "session") {
  activeTutorSideTab = tab;
  const buttons = tutorSidePanel ? Array.from(tutorSidePanel.querySelectorAll("[data-tutor-side-tab]")) : [];
  const panels = tutorSidePanel ? Array.from(tutorSidePanel.querySelectorAll("[data-tutor-side-panel]")) : [];
  buttons.forEach((button) => {
    const active = button.dataset.tutorSideTab === activeTutorSideTab;
    button.classList.toggle("active", active);
    button.setAttribute("aria-selected", active ? "true" : "false");
  });
  panels.forEach((panel) => {
    const active = panel.dataset.tutorSidePanel === activeTutorSideTab;
    panel.classList.toggle("hidden", !active);
    panel.setAttribute("aria-hidden", active ? "false" : "true");
  });
}

function toggleSidePanel() {
  if (!tutorTabLayout) {
    return;
  }
  tutorSidePanelCollapsed = !tutorSidePanelCollapsed;
  tutorTabLayout.classList.toggle("panel-collapsed", tutorSidePanelCollapsed);
  const btn = document.getElementById("panelToggleBtn");
  if (btn) {
    btn.textContent = tutorSidePanelCollapsed ? "<" : ">";
    btn.title = tutorSidePanelCollapsed ? "Open side panel" : "Collapse side panel";
  }
}

function updateTutorInputTopicChip() {
  const chip = document.getElementById("tutorCurrentTopicChip");
  if (!chip) {
    return;
  }
  const focus = getActiveTutorFocus();
  const text = focus.topic ? `${focus.topic} - ${focus.subject || "topic"}` : "No topic selected";
  chip.textContent = text;
}

function updateTutorSuggestedPromptsVisibility() {
  const chipRow = document.getElementById("tutorSmartPromptChips");
  const line = document.getElementById("tutorSmartPromptLine");
  const hasInput = !!(messageInput && String(messageInput.value || "").trim());
  if (chipRow) {
    chipRow.classList.toggle("hidden", hasInput);
  }
  if (line) {
    line.classList.toggle("hidden", hasInput);
  }
}

function toggleRecentChats() {
  const dropdown = document.getElementById("recent-chats-dropdown");
  if (!dropdown) {
    return;
  }
  dropdown.classList.toggle("hidden");
}

function renderTutorSideSessionSummary() {
  const topic = sessionStatsTopic ? sessionStatsTopic.textContent.replace(/^Current topic:\s*/, "") : "-";
  const confidence = sessionStatsConfidence ? sessionStatsConfidence.textContent : "new";
  const count = sessionStatsCount ? sessionStatsCount.textContent : "0";
  const average = sessionStatsAverage ? sessionStatsAverage.textContent : "0%";
  const streak = sessionStatsStreak ? sessionStatsStreak.textContent : "0";
  const target = document.getElementById("sideSessionSummary");
  if (!target) {
    return;
  }
  target.innerHTML = `
    <div class="side-session-summary-row"><span class="summary-label">Current topic</span><strong>${escapeHtml(topic || "-")}</strong></div>
    <div class="side-session-summary-grid">
      <div><span class="summary-label">Checkpoints</span><strong>${escapeHtml(count || "0")}</strong></div>
      <div><span class="summary-label">Average</span><strong>${escapeHtml(average || "0%")}</strong></div>
      <div><span class="summary-label">Streak</span><strong>${escapeHtml(streak || "0")}</strong></div>
    </div>
    <div class="side-session-summary-row"><span class="summary-label">Confidence</span><span class="pill">${escapeHtml(confidence || "new")}</span></div>
  `;
}

function buildTutorControlStrip() {
  if (!tutorTab || document.getElementById("tutorControlStrip")) {
    return;
  }

  const layout = document.createElement("div");
  layout.className = "tutor-tab-layout";
  layout.id = "tutorTabLayout";

  const strip = document.createElement("div");
  strip.className = "tutor-control-strip";
  strip.innerHTML = `
    <div class="tutor-strip-group">
      <button id="tutorVoiceToggleBtn" type="button" class="ghost-button compact-strip-btn" title="Voice on/off">Voice off</button>
      <button id="tutorSpeakToggleBtn" type="button" class="ghost-button compact-strip-btn" title="Auto-speak">Speak off</button>
      <button id="tutorCaptionToggleBtn" type="button" class="ghost-button compact-strip-btn" title="Captions">Captions on</button>
    </div>
    <div class="tutor-strip-group tutor-strip-center">
      <button id="tutorReadingToggleBtn" type="button" class="ghost-button compact-strip-btn" title="Reading comfort">Read off</button>
      <div class="tutor-pacing-toggle" role="group" aria-label="Pacing selector">
        <button id="tutorPaceGentleBtn" type="button" class="ghost-button compact-strip-btn" title="Gentle pacing">Gentle</button>
        <button id="tutorPaceNormalBtn" type="button" class="ghost-button compact-strip-btn" title="Normal pacing">Normal</button>
        <button id="tutorPaceFastBtn" type="button" class="ghost-button compact-strip-btn" title="Fast pacing">Fast</button>
      </div>
      <select id="tutorTopLevelSelect" class="compact-level-select" title="Tutor level">
        <option value="1">L1</option>
        <option value="2">L2</option>
        <option value="3" selected>L3</option>
        <option value="4">L4</option>
        <option value="5">L5</option>
      </select>
    </div>
    <div class="tutor-strip-group tutor-strip-right">
      <button id="tutorSpeakLastCompactBtn" type="button" class="ghost-button compact-strip-btn" title="Speak last reply">Speak</button>
      <button id="tutorPauseCompactBtn" type="button" class="ghost-button compact-strip-btn" title="Pause">Pause</button>
      <button id="tutorResumeCompactBtn" type="button" class="ghost-button compact-strip-btn" title="Resume">Resume</button>
      <button id="tutorStopCompactBtn" type="button" class="ghost-button compact-strip-btn" title="Stop and checkpoint">Stop</button>
      <button id="tutorFullscreenCompactBtn" type="button" class="ghost-button compact-strip-btn tutor-fullscreen-button" title="Expand to fullscreen">Fullscreen</button>
    </div>
  `;

  const chatZone = document.createElement("div");
  chatZone.className = "tutor-chat-zone";
  chatZone.id = "tutorChatZone";

  const sidePanel = document.createElement("aside");
  sidePanel.className = "tutor-side-panel";
  sidePanel.id = "tutorSidePanel";
  sidePanel.innerHTML = `
    <button id="panelToggleBtn" type="button" class="panel-toggle-btn" title="Collapse side panel"><</button>
    <div class="tutor-side-panel-tabs">
      <button type="button" class="active" data-tutor-side-tab="session" aria-selected="true">Session</button>
      <button type="button" data-tutor-side-tab="voice" aria-selected="false">Voice</button>
      <button type="button" data-tutor-side-tab="history" aria-selected="false">History</button>
      <button type="button" data-tutor-side-tab="video" aria-selected="false">Video</button>
    </div>
    <div class="tutor-side-panel-content">
      <div class="tutor-side-tab-panel" data-tutor-side-panel="session">
        <div class="table-card compact-side-card">
          <div class="card-header">
            <div>
              <p class="card-title">Session</p>
              <p class="muted">Current topic and progress at a glance.</p>
            </div>
          </div>
          <div id="sideSessionSummary"></div>
          <div class="side-panel-actions">
            <button id="sideStopCheckpointBtn" type="button" class="ghost-button">Stop & checkpoint</button>
            <button id="sideCompleteSessionBtn" type="button" class="ghost-button">Mark session complete</button>
          </div>
        </div>
        <div class="table-card compact-side-card">
          <div class="card-header">
            <div>
              <p class="card-title">Activity</p>
              <p class="muted">What Astra is doing in this session.</p>
            </div>
          </div>
          <div id="sessionActivityList" class="session-activity-list"></div>
        </div>
      </div>
      <div class="tutor-side-tab-panel hidden" data-tutor-side-panel="voice" aria-hidden="true">
        <div class="table-card compact-side-card">
          <div class="card-header">
            <div>
              <p class="card-title">Tutor Mode</p>
              <p class="muted">Compact persona controls for the tutor tone.</p>
            </div>
            <span id="tutorModePill" class="pill">Calm</span>
          </div>
          <div class="tutor-mode-pills" role="tablist" aria-label="Tutor mode">
            <button type="button" class="tutor-mode-pill active" data-tutor-mode="calm">Calm</button>
            <button type="button" class="tutor-mode-pill" data-tutor-mode="motivating">Motivating</button>
            <button type="button" class="tutor-mode-pill" data-tutor-mode="strict">Strict</button>
          </div>
        </div>
        <div class="table-card compact-side-card" id="tutorVoiceControlsMirror"></div>
      </div>
      <div class="tutor-side-tab-panel hidden" data-tutor-side-panel="history" aria-hidden="true">
        <div class="table-card compact-side-card">
          <div class="card-header">
            <div>
              <p class="card-title">Chats</p>
              <p class="muted">Rename, pin, or restore previous tutor conversations.</p>
            </div>
            <button id="newTutorChatBtnSide" type="button" class="ghost-button">New conversation</button>
          </div>
          <div id="tutorConversationList" class="conversation-list"></div>
          <div class="drawer-section">
            <p class="drawer-section-title">Recently deleted</p>
            <div id="deletedTutorConversationList" class="conversation-list"></div>
          </div>
          <div class="side-panel-actions">
            <button id="viewAllTutorChatsBtnSide" type="button" class="ghost-button">View all chats</button>
          </div>
        </div>
      </div>
      <div class="tutor-side-tab-panel hidden" data-tutor-side-panel="video" aria-hidden="true">
        <div class="table-card compact-side-card">
          <div class="card-header">
            <div>
              <p class="card-title">Video</p>
              <p class="muted">Jump to a video explanation from the current topic.</p>
            </div>
          </div>
          <div class="side-panel-actions">
            <button id="generateVideoFromTutorBtn" type="button" class="ghost-button">Generate video answer</button>
            <button id="openVideoTutorFromTutorBtn" type="button" class="ghost-button">Open Video Tutor</button>
          </div>
          <div id="tutorVideoPreviewMini" class="video-answer-brief-panel"></div>
        </div>
      </div>
    </div>
  `;

  const inputZone = document.createElement("div");
  inputZone.className = "tutor-input-zone";
  inputZone.id = "tutorInputZone";
  inputZone.innerHTML = `
    <div class="tutor-input-topline">
      <span id="tutorCurrentTopicChip" class="pill tutor-current-topic-chip">No topic selected</span>
      <span class="muted">Ask Astra anything and the workspace stays focused on the conversation.</span>
    </div>
    <div class="tutor-input-chip-row" id="tutorSmartPromptRow">
      <div id="tutorSmartPromptLine" class="muted tutor-smart-prompt-line">Suggested prompts will appear here.</div>
      <div id="tutorSmartPromptChips" class="tutor-suggested-chips"></div>
    </div>
  `;

  tutorTab.innerHTML = "";
  tutorTab.appendChild(layout);
  layout.appendChild(strip);
  layout.appendChild(chatZone);
  layout.appendChild(sidePanel);
  layout.appendChild(inputZone);

  chatZone.appendChild(sessionStatsCard);
  chatZone.appendChild(chapterResumeCard);
  chatZone.appendChild(chatFeed);
  chatZone.appendChild(kbStatusTag);

  inputZone.appendChild(chatForm);
  inputZone.appendChild(quickPromptGrid);
  if (tutorFullscreenBtn) {
    tutorFullscreenBtn.classList.add("hidden");
  }

  sidePanel.querySelector("[data-tutor-side-panel='session']").appendChild(sessionActivityPanel);
  if (sessionActivityPanel) {
    sessionActivityPanel.classList.remove("hidden");
  }
  sidePanel.querySelector("[data-tutor-side-panel='history']").appendChild(tutorConversationDrawerBackdrop);
  sidePanel.querySelector("[data-tutor-side-panel='history']").appendChild(tutorConversationDrawer);
  sidePanel.querySelector("[data-tutor-side-panel='video']").appendChild(tutorRoomLaunchCard);
  const voiceMirror = sidePanel.querySelector("#tutorVoiceControlsMirror");
  if (voiceMirror) {
    voiceMirror.appendChild(_buildTutorVoiceControlsMirror());
    voiceMirror.appendChild(tutorControlsBar);
    voiceMirror.appendChild(tutorModeCard);
  }

  const toggleBtn = sidePanel.querySelector("#panelToggleBtn");
  if (toggleBtn) {
    toggleBtn.addEventListener("click", toggleSidePanel);
  }
  sidePanel.querySelectorAll("[data-tutor-side-tab]").forEach((button) => {
    button.addEventListener("click", () => setTutorSidePanelTab(button.dataset.tutorSideTab));
  });

  const sessionTab = sidePanel.querySelector("[data-tutor-side-panel='session']");
  if (sessionTab) {
    const sessionActionRow = document.createElement("div");
    sessionActionRow.className = "side-panel-actions";
    const stopBtn = document.createElement("button");
    stopBtn.type = "button";
    stopBtn.className = "ghost-button";
    stopBtn.textContent = "Stop & checkpoint";
    stopBtn.addEventListener("click", () => {
      const tutorRoomStop = document.getElementById("tutorRoomStopBtn");
      if (tutorRoomStop) {
        tutorRoomStop.click();
      }
    });
    const completeBtn = document.createElement("button");
    completeBtn.type = "button";
    completeBtn.className = "ghost-button";
    completeBtn.textContent = "Mark session complete";
    completeBtn.addEventListener("click", () => {
      const checkpointScore = Math.round(Number(sessionCheckpointStats.average || 0));
      void completeJourneySessionFromCheckpoint(checkpointScore || 100);
    });
    sessionActionRow.append(stopBtn, completeBtn);
    sessionTab.insertBefore(sessionActionRow, sessionTab.querySelector(".session-activity-list"));
  }

  const historyTab = sidePanel.querySelector("[data-tutor-side-panel='history']");
  if (historyTab) {
    const viewAllBtn = document.getElementById("viewAllTutorChatsBtnSide");
    if (viewAllBtn) {
      viewAllBtn.addEventListener("click", () => {
        const drawerBackdrop = document.getElementById("tutorConversationDrawerBackdrop");
        const drawer = document.getElementById("tutorConversationDrawer");
        if (drawerBackdrop && drawer) {
          drawerBackdrop.classList.remove("hidden");
          drawer.classList.remove("hidden");
          drawer.setAttribute("aria-hidden", "false");
        }
      });
    }
    const newBtn = document.getElementById("newTutorChatBtnSide");
    if (newBtn) {
      newBtn.addEventListener("click", () => {
        const createBtn = document.getElementById("newTutorChatBtn");
        if (createBtn) {
          createBtn.click();
        }
      });
    }
  }

  const videoBtn = document.getElementById("generateVideoFromTutorBtn");
  if (videoBtn) {
    videoBtn.addEventListener("click", () => {
      if (videoTutorQuestionInput && !videoTutorQuestionInput.value.trim()) {
        const focus = getActiveTutorFocus();
        videoTutorQuestionInput.value = focus.topic || lastTutorQuestion || "";
      }
      const triggerBtn = generateVideoAnswerBtn || document.getElementById("videoAnswerBtn");
      if (triggerBtn) {
        triggerBtn.click();
      } else {
        void generateVideoAnswerBrief();
      }
    });
  }
  const openVideoBtn = document.getElementById("openVideoTutorFromTutorBtn");
  if (openVideoBtn) {
    openVideoBtn.addEventListener("click", () => setActiveTab("videoTutorTab"));
  }

  const stripToggle = document.getElementById("tutorFullscreenCompactBtn");
  if (stripToggle) {
    stripToggle.addEventListener("click", toggleTutorFullscreen);
  }
  const speakLast = document.getElementById("tutorSpeakLastCompactBtn");
  if (speakLast) {
    speakLast.addEventListener("click", () => {
      if (lastTutorReply) {
        speakText(lastTutorReply);
      }
    });
  }
  const pauseBtn = document.getElementById("tutorPauseCompactBtn");
  if (pauseBtn) {
    pauseBtn.addEventListener("click", () => pauseTutorNarration());
  }
  const resumeBtn = document.getElementById("tutorResumeCompactBtn");
  if (resumeBtn) {
    resumeBtn.addEventListener("click", () => resumeTutorNarration());
  }
  const stopBtn = document.getElementById("tutorStopCompactBtn");
  if (stopBtn) {
    stopBtn.addEventListener("click", () => interruptTutorOutput("tutor"));
  }
  const voiceToggle = document.getElementById("tutorVoiceToggleBtn");
  if (voiceToggle) {
    voiceToggle.addEventListener("click", () => {
      if (voiceChatMode) {
        voiceChatMode.checked = !voiceChatMode.checked;
        voiceChatMode.dispatchEvent(new Event("change", { bubbles: true }));
      }
    });
  }
  const speakToggle = document.getElementById("tutorSpeakToggleBtn");
  if (speakToggle) {
    speakToggle.addEventListener("click", () => {
      if (autoSpeakReplies) {
        autoSpeakReplies.checked = !autoSpeakReplies.checked;
        autoSpeakReplies.dispatchEvent(new Event("change", { bubbles: true }));
      }
    });
  }
  const captionToggle = document.getElementById("tutorCaptionToggleBtn");
  if (captionToggle) {
    captionToggle.addEventListener("click", () => {
      if (autoCaptionMode) {
        autoCaptionMode.checked = !autoCaptionMode.checked;
        autoCaptionMode.dispatchEvent(new Event("change", { bubbles: true }));
      }
    });
  }
  const readingToggle = document.getElementById("tutorReadingToggleBtn");
  if (readingToggle) {
    readingToggle.addEventListener("click", () => {
      if (readingComfortMode) {
        readingComfortMode.checked = !readingComfortMode.checked;
        readingComfortMode.dispatchEvent(new Event("change", { bubbles: true }));
      }
    });
  }
  ["tutorPaceGentleBtn", "tutorPaceNormalBtn", "tutorPaceFastBtn"].forEach((id) => {
    const btn = document.getElementById(id);
    if (btn) {
      btn.addEventListener("click", () => {
        if (!responsePacingSelect) {
          return;
        }
        if (id === "tutorPaceGentleBtn") responsePacingSelect.value = "gentle";
        if (id === "tutorPaceNormalBtn") responsePacingSelect.value = "standard";
        if (id === "tutorPaceFastBtn") responsePacingSelect.value = "fast";
        responsePacingSelect.dispatchEvent(new Event("change", { bubbles: true }));
      });
    }
  });
  const topLevel = document.getElementById("tutorTopLevelSelect");
  if (topLevel) {
    topLevel.addEventListener("change", () => {
      if (tutorLevelSelect) {
        tutorLevelSelect.value = topLevel.value;
        tutorLevelSelect.dispatchEvent(new Event("change", { bubbles: true }));
      }
    });
  }

  if (chatForm) {
    chatForm.classList.add("tutor-input-form");
  }

  if (messageInput) {
    messageInput.addEventListener("input", updateTutorSuggestedPromptsVisibility);
  }
  if (tutorTab) {
    tutorTab.dataset.tutorLayoutReady = "1";
  }

  tutorTabLayout = layout;
  tutorControlStrip = strip;
  tutorChatZone = chatZone;
  tutorSidePanel = sidePanel;
  tutorInputZone = inputZone;
  setTutorSidePanelTab("session");
  syncTutorControlStrip();
  updateTutorInputTopicChip();
  updateTutorSuggestedPromptsVisibility();
  renderTutorSideSessionSummary();
}

async function loadDailyBriefingIfNeeded(force = false) {
  if (!activeProfile) {
    return null;
  }
  const todayKey = new Date().toISOString().slice(0, 10);
  if (dailyBriefingDismissedDate === todayKey && !force) {
    return null;
  }
  if (!force && dailyBriefingLoadedDate === todayKey) {
    return null;
  }
  try {
    const response = await fetch("/api/ui/daily-briefing", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ student_id: activeProfile.name }),
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Could not load today's briefing.");
    }
    dailyBriefingLoadedDate = todayKey;
    const briefing = payload.briefing || {};
    renderDailyBriefingCard(briefing);
    return payload;
  } catch (error) {
    console.warn("Could not load daily briefing:", error);
    return null;
  }
}

async function loadProgressInsight() {
  if (!activeProfile) {
    return null;
  }
  try {
    const response = await fetch(`/api/analytics/dashboard/${encodeURIComponent(activeProfile.name)}`);
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Could not load analytics dashboard.");
    }
    renderAnalyticsDashboard(payload || {});
    return payload;
  } catch (error) {
    console.warn("Could not load analytics dashboard:", error);
    return null;
  }
}

function renderAnalyticsDashboard(payload) {
  const insightText = payload && payload.insight && payload.insight.insight ? payload.insight.insight : "";
  const trends = payload && payload.trends ? payload.trends : {};
  const weakStrong = payload && payload.weak_strong ? payload.weak_strong : {};
  const consistency = payload && payload.consistency ? payload.consistency : {};
  const subjectBreakdown = payload && payload.subject_breakdown ? payload.subject_breakdown : {};

  if (analyticsInsightCard) {
    const body = analyticsInsightCard.querySelector(".progress-insight-text");
    if (body) {
      body.textContent = insightText || "A personalized insight will appear here.";
    }
    analyticsInsightCard.classList.toggle("hidden", !insightText);
  }
  if (performanceChartSummary) {
    const weeklyImprovement = Number(trends.weekly_improvement || 0).toFixed(1);
    performanceChartSummary.textContent = trends.daily_scores && trends.daily_scores.length
      ? `Weekly improvement: ${weeklyImprovement}% | Best day: ${trends.best_day || "n/a"}`
      : "Your last 7 days of average scores will appear here.";
  }
  if (performanceChartBars) {
    performanceChartBars.innerHTML = "";
    const lastSeven = Array.isArray(trends.daily_scores) ? trends.daily_scores.slice(-7) : [];
    if (!lastSeven.length) {
      const empty = document.createElement("p");
      empty.className = "muted";
      empty.textContent = "No daily score data yet.";
      performanceChartBars.appendChild(empty);
    } else {
      const maxScore = Math.max(100, ...lastSeven.map((item) => Number(item.avg_score || 0)));
      lastSeven.forEach((item) => {
        const row = document.createElement("div");
        row.className = "performance-bar-row";
        const label = document.createElement("span");
        label.className = "performance-bar-label";
        label.textContent = item.date ? item.date.slice(5) : "Day";
        const track = document.createElement("div");
        track.className = "performance-bar-track";
        const fill = document.createElement("div");
        fill.className = "performance-bar-fill";
        fill.style.width = `${Math.max(6, Math.round((Number(item.avg_score || 0) / maxScore) * 100))}%`;
        const value = document.createElement("span");
        value.className = "performance-bar-value";
        value.textContent = `${Number(item.avg_score || 0).toFixed(0)}%`;
        track.appendChild(fill);
        row.append(label, track, value);
        performanceChartBars.appendChild(row);
      });
    }
  }

  if (subjectBreakdownGrid) {
    subjectBreakdownGrid.innerHTML = "";
    const order = ["physics", "chemistry", "mathematics"];
    order.forEach((subject) => {
      const data = subjectBreakdown[subject] || {};
      const card = document.createElement("div");
      card.className = "subject-breakdown-card";
      const mastery = Number(data.overall_mastery_percent || 0);
      card.innerHTML = `
        <div class="subject-circle" style="--progress:${Math.max(0, Math.min(100, mastery))}">
          <strong>${mastery.toFixed(0)}%</strong>
          <span>${subject.charAt(0).toUpperCase() + subject.slice(1)}</span>
        </div>
        <div class="subject-breakdown-list">
          <p class="muted">Total topics: ${Number(data.total_topics || 0)}</p>
          <p class="muted">Attempted: ${Number(data.topics_attempted || 0)}</p>
          <p class="muted">Strong: ${Number(data.topics_strong || 0)}</p>
          <p class="muted">Developing: ${Number(data.topics_developing || 0)}</p>
          <p class="muted">Weak: ${Number(data.topics_weak || 0)}</p>
          <p class="muted">Not started: ${Number(data.topics_not_started || 0)}</p>
        </div>
      `;
      subjectBreakdownGrid.appendChild(card);
    });
  }

  if (consistencyTrackerSummary) {
    consistencyTrackerSummary.textContent = `Current streak: ${Number(consistency.current_streak || 0)} day(s) | Consistency: ${Number(consistency.consistency_percent || 0).toFixed(0)}%`;
  }
  if (consistencyTrackerGrid) {
    consistencyTrackerGrid.innerHTML = "";
    const dailyScores = Array.isArray(trends.daily_scores) ? trends.daily_scores.slice(-7) : [];
    const dateSet = new Set(dailyScores.map((item) => item.date));
    const days = [];
    for (let offset = 6; offset >= 0; offset -= 1) {
      const day = new Date();
      day.setDate(day.getDate() - offset);
      const iso = day.toISOString().slice(0, 10);
      days.push(iso);
    }
    days.forEach((day) => {
      const circle = document.createElement("div");
      circle.className = `consistency-day ${dateSet.has(day) ? "studied" : "missed"}`;
      circle.title = day;
      circle.textContent = day.slice(8);
      consistencyTrackerGrid.appendChild(circle);
    });
  }

  if (chapterAnalyticsList) {
    chapterAnalyticsList.innerHTML = "";
    const addAnalyticsRow = (titleText, metaText) => {
      const row = document.createElement("div");
      row.className = "weekly-strategy-item";
      const title = document.createElement("strong");
      title.textContent = titleText;
      const meta = document.createElement("p");
      meta.className = "muted";
      meta.textContent = metaText;
      row.append(title, meta);
      chapterAnalyticsList.appendChild(row);
    };
    const dailyScores = Array.isArray(trends.daily_scores) ? trends.daily_scores : [];
    const formatTopicList = (items) => (Array.isArray(items) ? items : [])
      .slice(0, 5)
      .map((item) => {
        if (typeof item === "string") {
          return item;
        }
        const topic = item && (item.topic || item.unit_name || item.chapter_name);
        const score = item && (item.best_score ?? item.score ?? item.chapter_test_score);
        return topic ? `${topic}${score !== undefined && score !== null ? ` (${Number(score).toFixed(0)}%)` : ""}` : "";
      })
      .filter(Boolean);
    const weakTopics = formatTopicList(weakStrong.weak_topics);
    const strongTopics = formatTopicList(weakStrong.strong_topics);
    addAnalyticsRow(
      "Weak topics",
      weakTopics.length ? weakTopics.join(", ") : "No weak-topic signal yet."
    );
    addAnalyticsRow(
      "Strong topics",
      strongTopics.length ? strongTopics.join(", ") : "No strong-topic signal yet."
    );
  }
  if (chapterAnalyticsSummary) {
    chapterAnalyticsSummary.textContent = insightText || "Analytics dashboard loaded.";
  }
}

function setTutorMode(mode = "calm") {
  const normalizedMode = ["calm", "motivating", "strict"].includes(String(mode).trim().toLowerCase())
    ? String(mode).trim().toLowerCase()
    : "calm";
  activeTutorMode = normalizedMode;
  localStorage.setItem("alt_tutor_mode", normalizedMode);
  if (tutorModePill) {
    tutorModePill.textContent = normalizedMode.charAt(0).toUpperCase() + normalizedMode.slice(1);
  }
  if (tutorModeBadge) {
    tutorModeBadge.textContent = `${normalizedMode.charAt(0).toUpperCase() + normalizedMode.slice(1)} mode`;
  }
  tutorModeButtons.forEach((button) => {
    const isActive = button.dataset.tutorMode === normalizedMode;
    button.classList.toggle("active", isActive);
    button.setAttribute("aria-pressed", String(isActive));
  });
  syncTutorControlStrip();
}

function isLeagueTabEnabled() {
  return leagueTabVisible;
}

function getVisibleTabOrder() {
  return currentTabOrder.filter((key) => key !== "league" || isLeagueTabEnabled());
}

function renderDailyMotivation(studentName = "") {
  if (!dailyMotivationQuote) {
    return;
  }

  const now = new Date();
  const seed = `${now.getFullYear()}-${now.getMonth() + 1}-${now.getDate()}-${String(studentName || "").toLowerCase()}`;
  let hash = 0;
  for (let index = 0; index < seed.length; index += 1) {
    hash = (hash * 31 + seed.charCodeAt(index)) >>> 0;
  }

  dailyMotivationQuote.textContent = MOTIVATIONAL_QUOTES[hash % MOTIVATIONAL_QUOTES.length];
}

function _motivationDateIndex(length) {
  if (!length) {
    return 0;
  }
  const now = new Date();
  const seed = now.toISOString().slice(0, 10).replace(/-/g, "");
  let hash = 0;
  for (let index = 0; index < seed.length; index += 1) {
    hash = (hash * 31 + seed.charCodeAt(index)) >>> 0;
  }
  return hash % length;
}

function renderMotivationStory(index = activeMotivationStoryIndex) {
  if (!motivationStoryTitle || !motivationStoryBody || !motivationStoryStatus) {
    return;
  }
  if (!motivationStories.length) {
    motivationStoryTitle.textContent = "No story loaded yet";
    motivationStoryBody.innerHTML = "";
    motivationStoryBody.hidden = true;
    motivationStoryStatus.textContent = "0 of 0";
    if (motivationReadStoryBtn) {
      motivationReadStoryBtn.textContent = "Read a Story";
      motivationReadStoryBtn.disabled = true;
    }
    if (motivationPrevStoryBtn) motivationPrevStoryBtn.disabled = true;
    if (motivationNextStoryBtn) motivationNextStoryBtn.disabled = true;
    return;
  }

  const safeIndex = ((index % motivationStories.length) + motivationStories.length) % motivationStories.length;
  activeMotivationStoryIndex = safeIndex;
  const story = motivationStories[safeIndex] || {};
  motivationStoryTitle.textContent = story.title || `Story ${safeIndex + 1}`;
  motivationStoryStatus.textContent = `Story ${safeIndex + 1} of ${motivationStories.length}`;
  motivationStoryBody.innerHTML = story.story ? marked.parse(story.story) : "";
  motivationStoryBody.hidden = !motivationStoryOpen;
  if (motivationReadStoryBtn) {
    motivationReadStoryBtn.textContent = motivationStoryOpen ? "Hide Story" : "Read a Story";
    motivationReadStoryBtn.disabled = false;
  }
  if (motivationPrevStoryBtn) motivationPrevStoryBtn.disabled = motivationStories.length <= 1;
  if (motivationNextStoryBtn) motivationNextStoryBtn.disabled = motivationStories.length <= 1;
}

function renderMotivationBoosts(boosts = []) {
  if (!motivationBoostTokens) {
    return;
  }
  motivationBoostTokens.innerHTML = "";
  (boosts || []).slice(0, 3).forEach((token) => {
    const pill = document.createElement("span");
    pill.className = "motivation-token";
    pill.textContent = token;
    motivationBoostTokens.appendChild(pill);
  });
  if (!motivationBoostTokens.children.length) {
    const fallback = document.createElement("span");
    fallback.className = "motivation-token";
    fallback.textContent = "One concept at a time.";
    motivationBoostTokens.appendChild(fallback);
  }
}

async function fetchMotivationSection() {
  try {
    const [dailyResponse, storiesResponse] = await Promise.all([
      fetch("/api/motivation/daily"),
      fetch("/api/motivation/stories"),
    ]);
    const dailyPayload = await dailyResponse.json().catch(() => ({}));
    const storiesPayload = await storiesResponse.json().catch(() => ({}));
    if (dailyMotivationQuote) {
      dailyMotivationQuote.textContent = dailyPayload.quote || dailyMotivationQuote.textContent || "";
    }
    renderMotivationBoosts(dailyPayload.boost_tokens || []);
    motivationStories = Array.isArray(storiesPayload.stories) ? storiesPayload.stories : [];
    activeMotivationStoryIndex = motivationStories.length ? _motivationDateIndex(motivationStories.length) : 0;
    motivationStoryOpen = false;
    renderMotivationStory(activeMotivationStoryIndex);
  } catch (error) {
    console.warn("Could not load motivation section:", error);
    renderMotivationBoosts([]);
    motivationStories = [];
    activeMotivationStoryIndex = 0;
    motivationStoryOpen = false;
    renderMotivationStory(0);
  }
}

function applyLeagueVisibility() {
  if (showLeagueToggle) {
    showLeagueToggle.checked = leagueTabVisible;
  }

  const leagueButton = tabBar ? tabBar.querySelector('[data-tab-key="league"]') : null;
  const leaguePanel = document.getElementById("leagueTab");
  if (leagueButton) {
    leagueButton.classList.toggle("hidden", !leagueTabVisible);
    leagueButton.setAttribute("aria-hidden", leagueTabVisible ? "false" : "true");
  }
  if (leaguePanel) {
    leaguePanel.classList.toggle("hidden", !leagueTabVisible);
    leaguePanel.setAttribute("aria-hidden", leagueTabVisible ? "false" : "true");
  }

  if (!leagueTabVisible) {
    const activePanel = document.querySelector(".tab-panel.active");
    if (activePanel && activePanel.id === "leagueTab") {
      setActiveTab("overviewTab");
    }
  }

  localStorage.setItem("alt_show_league_tab", leagueTabVisible ? "1" : "0");
  refreshTabCollections();
  renderTabManager();
}

function setActiveStudioPane(paneId) {
  activeStudioPane = paneId || "threeConceptPanel";
  studioPaneButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.studioPane === activeStudioPane);
    button.setAttribute("aria-selected", button.dataset.studioPane === activeStudioPane ? "true" : "false");
  });
  studioPanes.forEach((pane) => {
    const isActive = pane.id === activeStudioPane;
    pane.classList.toggle("active", isActive);
    pane.hidden = !isActive;
    pane.setAttribute("aria-hidden", isActive ? "false" : "true");
  });
  window.dispatchEvent(new CustomEvent("alt:studio-pane-changed", { detail: { paneId: activeStudioPane } }));
  localStorage.setItem("alt_studio_pane", activeStudioPane);
}

function switchStudioTab(name) {
  setActiveStudioPane(name);
}

function focusTutorRoomStage(reason = "") {
  const videoTab = document.querySelector('.tab-button[data-tab="videoTutorTab"]');
  if (!videoTab || !videoTab.classList.contains("active")) {
    return;
  }
  if (activeStudioPane !== "threeTutorPanel") {
    setActiveStudioPane("threeTutorPanel");
  }
  ensureTutorRoomPersona();

  const panel = document.getElementById("threeTutorPanel");
  if (!panel) {
    return;
  }

  panel.classList.add("stage-focus-pulse");
  panel.dataset.focusReason = reason || "tutor";
  if (tutorStageFocusTimer) {
    window.clearTimeout(tutorStageFocusTimer);
  }
  tutorStageFocusTimer = window.setTimeout(() => {
    panel.classList.remove("stage-focus-pulse");
    delete panel.dataset.focusReason;
    tutorStageFocusTimer = null;
  }, 1800);
}

async function toggleStudioFullscreen() {
  const activePane = studioPanes.find((pane) => pane.id === activeStudioPane);
  if (!activePane) {
    return;
  }

  try {
    if (document.fullscreenElement === activePane) {
      await document.exitFullscreen();
    } else {
      await activePane.requestFullscreen();
    }
  } catch (error) {
    // Ignore fullscreen failures quietly.
  }
}

function _setTutorFullscreenButtonState(isFullscreen) {
  if (!tutorFullscreenBtn) {
    return;
  }
  tutorFullscreenBtn.textContent = isFullscreen ? "Exit fullscreen" : "Fullscreen";
  tutorFullscreenBtn.title = isFullscreen ? "Exit fullscreen" : "Expand to fullscreen";
  tutorFullscreenBtn.setAttribute("aria-label", isFullscreen ? "Exit fullscreen" : "Expand to fullscreen");
}

function exitTutorFullscreen() {
  if (!tutorChatPanel) {
    return;
  }
  tutorChatPanel.classList.remove("fullscreen-mode");
  _setTutorFullscreenButtonState(false);
  document.body.classList.remove("tutor-chat-fullscreen-active");
}

function toggleTutorFullscreen() {
  if (!tutorChatPanel) {
    return;
  }
  const isFullscreen = tutorChatPanel.classList.toggle("fullscreen-mode");
  document.body.classList.toggle("tutor-chat-fullscreen-active", isFullscreen);
  _setTutorFullscreenButtonState(isFullscreen);
}

function _setTutorFullscreenButtonState(isFullscreen) {
  if (!tutorFullscreenBtn) {
    return;
  }
  tutorFullscreenBtn.textContent = isFullscreen ? "Exit fullscreen" : "Fullscreen";
  tutorFullscreenBtn.title = isFullscreen ? "Exit fullscreen" : "Expand to fullscreen";
  tutorFullscreenBtn.setAttribute("aria-label", isFullscreen ? "Exit fullscreen" : "Expand to fullscreen");
}

function syncTutorFullscreenOverlay() {
  if (!tutorFullscreenOverlay || !tutorFullscreenMessages) {
    return;
  }
  if (chatFeed) {
    tutorFullscreenMessages.innerHTML = "";
    Array.from(chatFeed.children).forEach((node) => {
      if (node.classList && node.classList.contains("message")) {
        tutorFullscreenMessages.appendChild(node.cloneNode(true));
      }
    });
    tutorFullscreenMessages.scrollTop = tutorFullscreenMessages.scrollHeight;
  }
  if (tutorFullscreenTextarea && messageInput) {
    tutorFullscreenTextarea.value = messageInput.value || "";
  }
}

function exitTutorFullscreen() {
  if (!tutorFullscreenOverlay) {
    return;
  }
  tutorFullscreenOverlay.remove();
  tutorFullscreenOverlay = null;
  tutorFullscreenMessages = null;
  tutorFullscreenInputArea = null;
  tutorFullscreenTextarea = null;
  tutorFullscreenSendButton = null;
  _setTutorFullscreenButtonState(false);
}

function toggleTutorFullscreen() {
  if (tutorFullscreenOverlay) {
    exitTutorFullscreen();
    return;
  }
  if (!tutorChatPanel || !chatFeed || !messageInput) {
    return;
  }

  const overlay = document.createElement("div");
  overlay.className = "tutor-fullscreen-overlay";

  const exitButton = document.createElement("button");
  exitButton.type = "button";
  exitButton.className = "tutor-fullscreen-exit-btn ghost-button";
  exitButton.textContent = "Exit fullscreen";
  exitButton.addEventListener("click", exitTutorFullscreen);

  const messages = document.createElement("div");
  messages.className = "fullscreen-chat-messages";

  const inputArea = document.createElement("div");
  inputArea.className = "fullscreen-input-area";

  const fullscreenInput = messageInput.cloneNode(true);
  fullscreenInput.removeAttribute("id");
  fullscreenInput.classList.add("fullscreen-message-input");
  fullscreenInput.value = messageInput.value || "";

  const sendButtonSource = chatForm ? chatForm.querySelector('button[type="submit"]') : null;
  const fullscreenSendButton = sendButtonSource ? sendButtonSource.cloneNode(true) : document.createElement("button");
  fullscreenSendButton.type = "button";
  fullscreenSendButton.textContent = "Send";

  const sendFromOverlay = async () => {
    const value = String(fullscreenInput.value || "").trim();
    if (!value) {
      return;
    }
    messageInput.value = value;
    fullscreenInput.value = "";
    await sendMessage(value);
    syncTutorFullscreenOverlay();
  };

  fullscreenSendButton.addEventListener("click", sendFromOverlay);
  fullscreenInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendFromOverlay();
    }
  });

  inputArea.append(fullscreenInput, fullscreenSendButton);
  overlay.append(exitButton, messages, inputArea);
  document.body.appendChild(overlay);

  tutorFullscreenOverlay = overlay;
  tutorFullscreenMessages = messages;
  tutorFullscreenInputArea = inputArea;
  tutorFullscreenTextarea = fullscreenInput;
  tutorFullscreenSendButton = fullscreenSendButton;
  _setTutorFullscreenButtonState(true);
  syncTutorFullscreenOverlay();
  window.setTimeout(() => fullscreenInput.focus(), 0);
}

function _getTutorFullscreenSourceFeed() {
  return document.querySelector("#tutor-chat-messages, .tutor-messages, .chat-messages") || chatFeed;
}

function _setTutorFullscreenButtonState(isFullscreen) {
  if (!tutorFullscreenBtn) {
    return;
  }
  tutorFullscreenBtn.textContent = isFullscreen ? "Exit fullscreen" : "Fullscreen";
  tutorFullscreenBtn.title = isFullscreen ? "Exit fullscreen" : "Expand to fullscreen";
  tutorFullscreenBtn.setAttribute("aria-label", isFullscreen ? "Exit fullscreen" : "Expand to fullscreen");
}

function _cloneFullscreenMessageNode(node) {
  const clone = node.cloneNode(true);
  if (clone.classList) {
    if (clone.classList.contains("student")) {
      clone.classList.add("message-student");
    }
    if (clone.classList.contains("tutor")) {
      clone.classList.add("message-tutor");
    }
  }
  return clone;
}

function syncTutorFullscreenOverlay() {
  if (!tutorFullscreenOverlay || !tutorFullscreenMessages) {
    return;
  }
  const sourceFeed = tutorFullscreenMirrorSource || _getTutorFullscreenSourceFeed();
  if (sourceFeed) {
    tutorFullscreenMessages.innerHTML = "";
    Array.from(sourceFeed.children).forEach((node) => {
      if (node.classList && node.classList.contains("message")) {
        tutorFullscreenMessages.appendChild(_cloneFullscreenMessageNode(node));
      }
    });
    tutorFullscreenMessages.scrollTop = tutorFullscreenMessages.scrollHeight;
  }
  if (tutorFullscreenTextarea && messageInput) {
    tutorFullscreenTextarea.value = messageInput.value || "";
  }
}

function closeTutorFullscreen() {
  if (tutorFullscreenMirrorObserver) {
    tutorFullscreenMirrorObserver.disconnect();
    tutorFullscreenMirrorObserver = null;
  }
  tutorFullscreenMirrorSource = null;
  if (tutorFullscreenOverlay) {
    tutorFullscreenOverlay.remove();
  }
  tutorFullscreenOverlay = null;
  tutorFullscreenMessages = null;
  tutorFullscreenInputArea = null;
  tutorFullscreenTextarea = null;
  tutorFullscreenSendButton = null;
  _setTutorFullscreenButtonState(false);
}

function fsSendMessage() {
  const input = document.getElementById("fs-input");
  if (!input || !input.value.trim()) {
    return;
  }
  const text = input.value.trim();
  input.value = "";

  const messagesArea = document.getElementById("fs-messages-area");
  if (messagesArea) {
    const studentMsg = document.createElement("div");
    studentMsg.className = "message-student";
    studentMsg.textContent = text;
    messagesArea.appendChild(studentMsg);
    messagesArea.scrollTop = messagesArea.scrollHeight;
  }

  const realInput = document.querySelector("#tutor-input, .tutor-input, [placeholder*=\"academic\"]") || messageInput;
  if (realInput) {
    realInput.value = text;
  }

  const sendBtn = chatForm ? chatForm.querySelector('button[type="submit"]') : null;
  if (sendBtn) {
    sendBtn.click();
  } else {
    void sendMessage(text);
  }

  syncTutorFullscreenOverlay();
}

function openTutorFullscreen() {
  if (tutorFullscreenOverlay) {
    return;
  }
  if (!tutorChatPanel || !messageInput) {
    return;
  }

  const overlay = document.createElement("div");
  overlay.className = "tutor-fullscreen-overlay";
  overlay.id = "tutor-fullscreen-overlay";

  const topbar = document.createElement("div");
  topbar.className = "tutor-fullscreen-topbar";
  topbar.innerHTML = `
    <span class="fs-title">Astra Tutor</span>
    <button class="tutor-fullscreen-exit-btn" onclick="closeTutorFullscreen()">Exit fullscreen</button>
  `;

  const messagesArea = document.createElement("div");
  messagesArea.className = "tutor-fullscreen-messages";
  messagesArea.id = "fs-messages-area";

  tutorFullscreenMirrorSource = _getTutorFullscreenSourceFeed();
  if (tutorFullscreenMirrorSource) {
    Array.from(tutorFullscreenMirrorSource.children).forEach((node) => {
      if (node.classList && node.classList.contains("message")) {
        messagesArea.appendChild(_cloneFullscreenMessageNode(node));
      }
    });
  }

  window.setTimeout(() => {
    messagesArea.scrollTop = messagesArea.scrollHeight;
  }, 100);

  const inputArea = document.createElement("div");
  inputArea.className = "tutor-fullscreen-input-area";
  inputArea.innerHTML = `
    <textarea id="fs-input" placeholder="Ask your tutor..." rows="1" onkeydown="if(event.key==='Enter' && !event.shiftKey){event.preventDefault();fsSendMessage()}"></textarea>
    <button class="tutor-fullscreen-send-btn" onclick="fsSendMessage()">Send</button>
  `;

  overlay.appendChild(topbar);
  overlay.appendChild(messagesArea);
  overlay.appendChild(inputArea);
  document.body.appendChild(overlay);

  tutorFullscreenOverlay = overlay;
  tutorFullscreenMessages = messagesArea;
  tutorFullscreenInputArea = inputArea;
  tutorFullscreenTextarea = overlay.querySelector("#fs-input");
  tutorFullscreenSendButton = inputArea.querySelector(".tutor-fullscreen-send-btn");
  _setTutorFullscreenButtonState(true);

  if (tutorFullscreenMirrorObserver) {
    tutorFullscreenMirrorObserver.disconnect();
  }
  if (tutorFullscreenMirrorSource) {
    tutorFullscreenMirrorObserver = new MutationObserver(() => {
      if (!tutorFullscreenOverlay) {
        return;
      }
      syncTutorFullscreenOverlay();
    });
    tutorFullscreenMirrorObserver.observe(tutorFullscreenMirrorSource, { childList: true, subtree: true });
  }

  syncTutorFullscreenOverlay();
  window.setTimeout(() => tutorFullscreenTextarea && tutorFullscreenTextarea.focus(), 200);
}

function toggleTutorFullscreen() {
  if (tutorFullscreenOverlay) {
    closeTutorFullscreen();
    return;
  }
  openTutorFullscreen();
}

function _setLoungeFullscreenButtonState(isFullscreen) {
  if (!loungeFullscreenBtn) {
    return;
  }
  loungeFullscreenBtn.textContent = isFullscreen ? "Exit fullscreen" : "Fullscreen";
  loungeFullscreenBtn.title = isFullscreen ? "Exit lounge fullscreen" : "Expand lounge to fullscreen";
  loungeFullscreenBtn.setAttribute("aria-label", isFullscreen ? "Exit lounge fullscreen" : "Expand lounge to fullscreen");
}

function syncLoungeFullscreenOverlay() {
  if (!loungeFullscreenOverlay || !loungeFullscreenMessages) {
    return;
  }
  const sourceFeed = loungeFullscreenMirrorSource || loungeFeed;
  if (sourceFeed) {
    loungeFullscreenMessages.innerHTML = "";
    Array.from(sourceFeed.children).forEach((node) => {
      if (node.classList && node.classList.contains("message")) {
        loungeFullscreenMessages.appendChild(_cloneFullscreenMessageNode(node));
      }
    });
    loungeFullscreenMessages.scrollTop = loungeFullscreenMessages.scrollHeight;
  }
  if (loungeFullscreenTextarea && loungeMessageInput) {
    loungeFullscreenTextarea.value = loungeMessageInput.value || "";
  }
}

function closeLoungeFullscreen() {
  if (loungeFullscreenMirrorObserver) {
    loungeFullscreenMirrorObserver.disconnect();
    loungeFullscreenMirrorObserver = null;
  }
  loungeFullscreenMirrorSource = null;
  if (loungeFullscreenOverlay) {
    loungeFullscreenOverlay.remove();
  }
  loungeFullscreenOverlay = null;
  loungeFullscreenMessages = null;
  loungeFullscreenTextarea = null;
  _setLoungeFullscreenButtonState(false);
}

async function sendLoungeFullscreenMessage() {
  if (!loungeFullscreenTextarea || !loungeMessageInput) {
    return;
  }
  const text = loungeFullscreenTextarea.value.trim();
  if (!text) {
    return;
  }
  loungeFullscreenTextarea.value = "";
  loungeMessageInput.value = text;
  setActiveTab("loungeTab");
  await sendMessage(text);
  loungeMessageInput.value = "";
  syncLoungeFullscreenOverlay();
}

function openLoungeFullscreen() {
  if (loungeFullscreenOverlay) {
    return;
  }
  if (!loungeFeed || !loungeMessageInput) {
    return;
  }

  const overlay = document.createElement("div");
  overlay.className = "tutor-fullscreen-overlay";
  overlay.id = "lounge-fullscreen-overlay";

  const topbar = document.createElement("div");
  topbar.className = "tutor-fullscreen-topbar";

  const title = document.createElement("span");
  title.className = "fs-title";
  title.textContent = "Astra Lounge";

  const exitButton = document.createElement("button");
  exitButton.type = "button";
  exitButton.className = "tutor-fullscreen-exit-btn";
  exitButton.textContent = "Exit fullscreen";
  exitButton.addEventListener("click", closeLoungeFullscreen);
  topbar.append(title, exitButton);

  const messagesArea = document.createElement("div");
  messagesArea.className = "tutor-fullscreen-messages";

  const inputArea = document.createElement("div");
  inputArea.className = "tutor-fullscreen-input-area";

  const textarea = loungeMessageInput.cloneNode(true);
  textarea.removeAttribute("id");
  textarea.removeAttribute("style");
  textarea.value = loungeMessageInput.value || "";
  textarea.placeholder = "Talk in Lounge...";
  textarea.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      void sendLoungeFullscreenMessage();
    }
  });

  const sendButton = document.createElement("button");
  sendButton.type = "button";
  sendButton.className = "tutor-fullscreen-send-btn";
  sendButton.textContent = "Send";
  sendButton.addEventListener("click", () => {
    void sendLoungeFullscreenMessage();
  });

  inputArea.append(textarea, sendButton);
  overlay.append(topbar, messagesArea, inputArea);
  document.body.appendChild(overlay);

  loungeFullscreenOverlay = overlay;
  loungeFullscreenMessages = messagesArea;
  loungeFullscreenTextarea = textarea;
  loungeFullscreenMirrorSource = loungeFeed;
  _setLoungeFullscreenButtonState(true);

  if (loungeFullscreenMirrorObserver) {
    loungeFullscreenMirrorObserver.disconnect();
  }
  loungeFullscreenMirrorObserver = new MutationObserver(() => {
    if (loungeFullscreenOverlay) {
      syncLoungeFullscreenOverlay();
    }
  });
  loungeFullscreenMirrorObserver.observe(loungeFeed, { childList: true, subtree: true });

  syncLoungeFullscreenOverlay();
  window.setTimeout(() => loungeFullscreenTextarea && loungeFullscreenTextarea.focus(), 0);
}

function toggleLoungeFullscreen() {
  if (loungeFullscreenOverlay) {
    closeLoungeFullscreen();
    return;
  }
  openLoungeFullscreen();
}

function setAuthMode(mode) {
  const signinActive = mode === "signin";
  signinPanel.classList.toggle("hidden", !signinActive);
  signupPanel.classList.toggle("hidden", signinActive);
  showSigninBtn.classList.toggle("active-switch", signinActive);
  showSignupBtn.classList.toggle("active-switch", !signinActive);
  updateExamBrandCopy(activeProfile, mode);
  profileStatus.textContent = signinActive
    ? "Your dashboard will open after the profile is loaded."
    : "Create your profile and continue into the app.";
}

function buildAstraPixels() {
  if (!astraPixels) {
    return;
  }

  const letters = ["A", "S", "T", "R", "A"];
  const letterWidth = 5;
  const letterHeight = 7;
  const gapWidth = 1;
  const totalColumns = letters.length * letterWidth + (letters.length - 1) * gapWidth;
  astraPixels.innerHTML = "";
  astraPixels.style.gridTemplateColumns = `repeat(${totalColumns}, minmax(0, 1fr))`;

  for (let row = 0; row < letterHeight; row += 1) {
    for (let col = 0; col < totalColumns; col += 1) {
      const pixel = document.createElement("span");
      const letterIndex = Math.floor(col / (letterWidth + gapWidth));
      const offsetWithinBlock = col % (letterWidth + gapWidth);
      const letter = letters[letterIndex];
      const isLetterCell = offsetWithinBlock < letterWidth;
      const active = isLetterCell && ASTRA_PIXEL_PATTERNS[letter][row][offsetWithinBlock] === "1";
      pixel.className = "astra-pixel is-dim";
      const spread = Math.min(window.innerWidth || 1600, window.innerHeight || 900) * 0.18;
      const scatterX = (Math.random() * 2 - 1) * Math.min(spread, 220);
      const scatterY = (Math.random() * 2 - 1) * Math.min(spread, 220);
      pixel.style.setProperty("--scatter-x", `${scatterX.toFixed(1)}px`);
      pixel.style.setProperty("--scatter-y", `${scatterY.toFixed(1)}px`);
      const delay = window.matchMedia("(prefers-reduced-motion: reduce)").matches
        ? 0
        : (row * totalColumns + col) * 8;
      pixel.style.setProperty("--delay", `${delay}ms`);
      astraPixels.appendChild(pixel);
      if (active) {
        window.setTimeout(() => {
          if (!pixel.isConnected) {
            return;
          }
          pixel.classList.add("is-active");
        }, delay);
      }
    }
  }
}

function revealLoginFromSplash() {
  if (!splashScreen || splashScreen.classList.contains("hidden") || splashDismissed) {
    return;
  }

  splashDismissed = true;
  splashScreen.classList.add("hidden");
  loginScreen.classList.remove("hidden");
  setAuthMode("signin");
  window.requestAnimationFrame(() => {
    if (signinEmailInput) {
      signinEmailInput.focus();
    }
  });
}

function initializeAstraSplash() {
  if (!splashScreen) {
    return;
  }

  buildAstraPixels();
  window.setTimeout(() => {
    if (splashScreen && !splashScreen.classList.contains("hidden")) {
      splashScreen.classList.add("splash-ready");
    }
  }, 340);
  window.setTimeout(() => {
    if (splashScreen && !splashScreen.classList.contains("hidden")) {
      splashScreen.classList.add("splash-cta-ready");
    }
  }, 1120);
}

function normalizeTutorTrait(value) {
  return String(value || "").trim().toLowerCase();
}

function renderTutorTraitChips(selectedTraits = []) {
  if (!tutorTraitChips) {
    return;
  }

  const selected = new Set(selectedTraits.map(normalizeTutorTrait).filter(Boolean));
  tutorTraitChips.innerHTML = "";

  TUTOR_PERSONALITY_TRAITS.forEach((trait) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `soft-chip${selected.has(trait.key) ? " active" : ""}`;
    button.textContent = trait.label;
    button.dataset.traitKey = trait.key;
    button.addEventListener("click", () => {
      const next = new Set(selectedTutorTraits.map(normalizeTutorTrait).filter(Boolean));
      if (next.has(trait.key)) {
        next.delete(trait.key);
      } else {
        next.add(trait.key);
      }
      selectedTutorTraits = Array.from(next);
      renderTutorTraitChips(selectedTutorTraits);
      updateTutorSummary(activeProfile || {});
    });
    tutorTraitChips.appendChild(button);
  });
}

function applyTutorPersonalityToForm(profile) {
  if (!profile) {
    selectedTutorTraits = [];
    renderTutorTraitChips([]);
    return;
  }

  if (tutorPersonaPresetSelect) {
    tutorPersonaPresetSelect.value = profile.tutor_personality_preset || "balanced";
  }
  if (tutorStyleInput) {
    tutorStyleInput.value = profile.tutor_personality_notes || profile.tutor_style || "";
  }
  selectedTutorTraits = Array.isArray(profile.tutor_personality_traits)
    ? profile.tutor_personality_traits
    : [];
  renderTutorTraitChips(selectedTutorTraits);
}

function buildTutorStyleSummary() {
  const preset = tutorPersonaPresetSelect ? tutorPersonaPresetSelect.value || "balanced" : "balanced";
  const traits = selectedTutorTraits.length ? selectedTutorTraits.join(", ") : "none";
  const notes = (tutorStyleInput && tutorStyleInput.value.trim()) || "";
  const parts = [`preset: ${preset}`, `traits: ${traits}`];
  if (notes) {
    parts.push(`notes: ${notes}`);
  }
  return parts.join(" | ");
}

function updateTutorSummary(profile) {
  const tutorName = (profile && profile.tutor_name) || "Astra";
  const tutorStyle = (profile && profile.tutor_style) || "positive, encouraging, and easy to talk to";
  const appearance = (profile && profile.appearance_description) || "friendly, fun, and human-like";
  const preset = (profile && profile.tutor_personality_preset) || "balanced";
  const traits = Array.isArray(profile && profile.tutor_personality_traits)
    ? profile.tutor_personality_traits.join(", ")
    : "";
  const traitLine = traits ? ` Traits: ${traits}.` : "";
  const examLabel = getActiveExamLabel(profile);
  const examLine = examLabel && examLabel !== "your exam" ? ` Current focus: ${examLabel}.` : "";
  const summary = `${tutorName} is set to ${preset} mode.${traitLine}${examLine} Notes: ${tutorStyle}. Looks ${appearance}.`;

  if (tutorStudioSummary) {
    tutorStudioSummary.textContent = summary;
  }
  if (sidebarTutorSummary) {
    sidebarTutorSummary.textContent = summary;
  }
}

  function renderTutorBrain(brain) {
    activeTutorBrain = brain || null;
    updateTutorRoomLivePanel();
  }

  function setAvatarStatusText(text) {
    const value = String(text || "Ready").trim() || "Ready";
    if (avatarStatusText) {
      avatarStatusText.textContent = value;
    }
    if (avatarStageStatus) {
      avatarStageStatus.textContent = value;
    }
  }

  function getAvatarConfigUrl() {
    return "/avatars/avatar_config.json";
  }

  async function loadStudentProfile() {
    if (activeProfile) {
      return activeProfile;
    }
    const name = activeUser?.name || activeUser?.student_name || "";
    if (!name) {
      return null;
    }
    try {
      const response = await fetch(`/api/profile/${encodeURIComponent(name)}`);
      const payload = await response.json();
      if (!response.ok) {
        return null;
      }
      return payload.profile || null;
    } catch (error) {
      console.warn("Could not load student profile for avatar stage:", error);
      return null;
    }
  }

  async function loadAvatarConfig() {
    if (avatarConfigCache) {
      return avatarConfigCache;
    }
    try {
      const response = await fetch(getAvatarConfigUrl());
      const payload = await response.json();
      avatarConfigCache = payload && Array.isArray(payload.avatars) ? payload : { avatars: [] };
      return avatarConfigCache;
    } catch (error) {
      console.warn("Could not load avatar config:", error);
      avatarConfigCache = { avatars: [] };
      return avatarConfigCache;
    }
  }

  function normalizeAvatarId(value) {
    return String(value || "").trim().toLowerCase().replace(/_/g, "-");
  }

  function getAvatarConfigForTutorId(config, tutorId) {
    const avatars = (config && Array.isArray(config.avatars) ? config.avatars : []).filter(Boolean);
    if (!avatars.length) {
      return null;
    }
    const normalizedId = normalizeAvatarId(tutorId);
    return avatars.find((avatar) => normalizeAvatarId(avatar.id) === normalizedId) || avatars[0] || null;
  }

  async function initAvatar() {
    try {
      if (!avatarCanvas || !window.AvatarRenderer) {
        return null;
      }
      if (avatarStageInitPromise) {
        return avatarStageInitPromise;
      }

      avatarStageInitPromise = (async () => {
        const profile = await loadStudentProfile();
        const config = await loadAvatarConfig();
        const avatarConfig = getAvatarConfigForTutorId(config, profile?.selected_avatar || profile?.tutor_id || "calm-mentor");
        if (!avatarConfig) {
          return null;
        }

        if (!avatarRenderer) {
          avatarRenderer = new AvatarRenderer("avatar-canvas");
          await avatarRenderer.init();
          window.addEventListener("resize", () => {
            if (!avatarRenderer || !avatarCanvas) {
              return;
            }
            avatarRenderer.resize(avatarCanvas.clientWidth || 400, avatarCanvas.clientHeight || 500);
          });
        }

        if (avatarNameBadge) {
          avatarNameBadge.textContent = avatarConfig.name || "Calm Mentor";
        }
        setAvatarStatusText("Loading avatar...");

        try {
          await avatarRenderer.loadAvatar(avatarConfig.glb_url);
          avatarRenderer.canvas.style.display = "block";
          setAvatarStatusText("Ready");
        } catch (error) {
          console.log("GLB not found, using 2D fallback:", error);
          avatarRenderer.useFallback2D(avatarConfig.fallback_image || "");
          setAvatarStatusText("Ready");
        }

        return avatarRenderer;
      })();

      const instance = await avatarStageInitPromise;
      return instance;
    } catch (error) {
      console.error("Avatar init failed:", error);
      setAvatarStatusText("Ready");
      return null;
    } finally {
      avatarStageInitPromise = null;
    }
  }

  function avatarSpeak(text) {
    const textToSpeak = String(text || lastTutorReplyText || lastTutorReply || (activeAvatar && activeAvatar.sample_line) || "").trim();
    if (!textToSpeak) {
      return;
    }
    if (!supportsSpeech()) {
      setAvatarStatusText("Voice unavailable");
      return;
    }
    lastTutorReplyText = textToSpeak;
    if (avatarRenderer) {
      avatarRenderer.startSpeakingAnimation();
    }
    setAvatarStatusText("Speaking...");
    speakText(textToSpeak);
  }

  function avatarStop() {
    window.speechSynthesis.cancel();
    if (avatarRenderer) {
      avatarRenderer.stopSpeakingAnimation();
    }
    setAvatarStatusText("Ready");
    stopTalkingFace();
    setCaption("Speech stopped.");
    if (activeSpeechUtterance) {
      activeSpeechUtterance = null;
    }
    updateTutorRoomLivePanel();
  }

  function onTutorReplyReceived(replyText) {
    lastTutorReplyText = String(replyText || "").trim();
  }

function updateTutorRoomLivePanel() {
  if (!tutorRoomLivePill || !tutorRoomLiveSummary) {
    return;
  }

  const voiceOn = !!(voiceChatMode && voiceChatMode.checked);
  const speakOn = !!(autoSpeakReplies && autoSpeakReplies.checked);
  const captionOn = !!(autoCaptionMode && autoCaptionMode.checked);
  const readingOn = !!(readingComfortMode && readingComfortMode.checked);
  const chunkedOn = !!(chunkedReplyMode && chunkedReplyMode.checked);
  const pacingMode = (responsePacingSelect && responsePacingSelect.value) || "standard";
  const tutorLevel = Number((tutorLevelSelect && tutorLevelSelect.value) || "3");
  const narration = activeTutorNarration && activeTutorNarration.mode === "tutor" ? activeTutorNarration : null;
  const checkpoint = tutorReplyCheckpoints.tutor;
  const lastReply = (lastRepliesByMode.tutor || lastTutorReply || "").trim();
  const liveState = narration
    ? (narration.paused ? "Paused" : "Live")
    : (lastReply ? "Ready" : "Ready");
  const liveLine = narration
    ? (narration.paused
      ? "Astra is paused at a checkpoint. Press Resume or Esc to continue naturally."
      : "Astra is speaking. Interrupt at any time and keep the checkpoint.")
    : (lastReply
      ? "Astra is ready for your next question. You can ask for a follow-up or a different explanation level."
      : "Speak or type a doubt and Astra will answer here like a live teacher.");

  tutorRoomLivePill.textContent = liveState;
  const accessibilitySummary = readingOn
    ? " Reading comfort and pacing controls are active."
    : "";
  tutorRoomLiveSummary.textContent = (voiceOn
    ? "Voice mode is on, so Astra will answer in a more spoken, conversational style."
    : "Text mode is on, so Astra will keep replies clear and easy to read.") + accessibilitySummary;

  if (tutorRoomVoiceState) {
    tutorRoomVoiceState.textContent = voiceOn ? "Voice on" : "Voice off";
  }
  if (tutorRoomSpeakState) {
    tutorRoomSpeakState.textContent = speakOn ? "Auto-speak on" : "Auto-speak off";
  }
  if (tutorRoomCaptionState) {
    tutorRoomCaptionState.textContent = captionOn ? "Captions on" : "Captions off";
  }
  if (tutorRoomReadState) {
    tutorRoomReadState.textContent = readingOn ? "Reading comfort on" : "Reading comfort off";
  }
  if (tutorRoomPaceState) {
    const paceLabel = pacingMode === "slow" ? "Pacing slow" : pacingMode === "gentle" ? "Pacing gentle" : "Pacing standard";
    tutorRoomPaceState.textContent = chunkedOn ? `${paceLabel} - chunked` : paceLabel;
  }
  if (tutorRoomLevelState) {
    tutorRoomLevelState.textContent = `Level ${tutorLevel}`;
  }
  if (generateVideoAnswerBtn) {
    const hasQuestion = !!(lastTutorQuestion.trim() || lastTutorReply.trim());
    generateVideoAnswerBtn.disabled = !hasQuestion;
    generateVideoAnswerBtn.textContent = "Generate";
  }
  if (tutorRoomLiveHint) {
    tutorRoomLiveHint.textContent = liveLine;
  }
  if (tutorRoomPauseBtn) {
    tutorRoomPauseBtn.disabled = !(narration && !narration.paused);
  }
  if (tutorRoomResumeBtn) {
    tutorRoomResumeBtn.disabled = !(narration ? narration.paused : !!checkpoint);
  }
  if (tutorRoomStopBtn) {
    tutorRoomStopBtn.disabled = !narration && !lastReply;
  }
  if (tutorRoomSpeakLastBtn) {
    tutorRoomSpeakLastBtn.disabled = !lastReply;
  }
  if (tutorRoomMessageInput) {
    tutorRoomMessageInput.placeholder = voiceOn
      ? "Talk to Astra like a live tutor. You can interrupt, resume, or ask for a different explanation level..."
      : "Type your doubt here. Astra will still answer in a direct tutor style...";
  }
}

function renderVideoAnswerBrief(brief) {
  lastVideoAnswerBrief = brief || null;
  if (!brief) {
    if (videoAnswerBriefPanel) {
      videoAnswerBriefPanel.innerHTML = "";
    }
    setVideoTutorStatus("Astra is waiting for a video answer request.", { visible: true });
    if (videoRenderStatus) {
      videoRenderStatus.textContent = "Generate a video answer to launch the full tutor video pipeline.";
    }
    showToast("Astra is waiting for a video answer request.", "success");
    if (videoTranscriptPanel) {
      videoTranscriptPanel.textContent = "";
    }
    return;
  }

  if (videoAnswerBriefPanel) {
    videoAnswerBriefPanel.innerHTML = "";
    const header = document.createElement("div");
    header.className = "video-answer-brief-header";

    const titleBlock = document.createElement("div");
    const title = document.createElement("p");
    title.className = "card-title";
    title.textContent = `${brief.tutor_face?.name || "Astra Tutor"} video answer`;
    const meta = document.createElement("p");
    meta.className = "muted";
    meta.textContent = `${brief.subject || "JEE"} | ${brief.topic || "Concept"} | Level ${brief.tutor_level || 3} | ${brief.expected_duration_seconds || 0}s`;
    titleBlock.appendChild(title);
    titleBlock.appendChild(meta);

    const status = document.createElement("span");
    status.className = "pill";
    status.textContent = brief.status || "brief_ready";
    header.appendChild(titleBlock);
    header.appendChild(status);
    videoAnswerBriefPanel.appendChild(header);

    const question = document.createElement("p");
    question.className = "video-answer-brief-question";
    question.textContent = brief.question ? `Question: ${brief.question}` : "Question not available.";
    videoAnswerBriefPanel.appendChild(question);

    const voice = document.createElement("p");
    voice.className = "muted";
    const voiceStyle = brief.voice_style || {};
    voice.textContent = `Voice: ${voiceStyle.avatar_name || "Astra Tutor"} | ${voiceStyle.assistant_voice_family || "female"} | ${voiceStyle.speaking_style || "clear and warm"}`;
    videoAnswerBriefPanel.appendChild(voice);

    const scriptHeading = document.createElement("p");
    scriptHeading.className = "memory-heading";
    scriptHeading.textContent = "Script blocks";
    videoAnswerBriefPanel.appendChild(scriptHeading);

    const scriptList = document.createElement("div");
    scriptList.className = "video-answer-brief-list";
    (brief.script_blocks || []).forEach((block) => {
      const item = document.createElement("div");
      item.className = "video-answer-brief-item";
      const itemTitle = document.createElement("p");
      itemTitle.className = "memory-heading";
      itemTitle.textContent = block.label || "Scene";
      const itemText = document.createElement("p");
      itemText.className = "muted";
      itemText.textContent = block.text || "";
      item.appendChild(itemTitle);
      item.appendChild(itemText);
      scriptList.appendChild(item);
    });
    videoAnswerBriefPanel.appendChild(scriptList);

    const sceneHeading = document.createElement("p");
    sceneHeading.className = "memory-heading";
    sceneHeading.textContent = "Scene and gesture plan";
    videoAnswerBriefPanel.appendChild(sceneHeading);

    (brief.scene_blocks || []).forEach((scene) => {
      const sceneItem = document.createElement("p");
      sceneItem.className = "muted";
      sceneItem.textContent = `${scene.label || "Scene"}: ${scene.narration || ""}${scene.gesture ? ` | Gesture: ${scene.gesture}` : ""}`;
      videoAnswerBriefPanel.appendChild(sceneItem);
    });

    const note = document.createElement("p");
    note.className = "muted";
    note.textContent = Array.isArray(brief.gesture_notes) && brief.gesture_notes.length
      ? `Gesture notes: ${brief.gesture_notes.join(" ")}`
      : "Gesture notes will appear here.";
    videoAnswerBriefPanel.appendChild(note);
  }
  if (videoTranscriptPanel) {
    videoTranscriptPanel.textContent = brief.recap || brief.caption_text || "The recap will appear here when Astra renders the answer.";
  }
  if (videoRenderStatus) {
    videoRenderStatus.textContent = "The tutor video brief is ready. Astra can now launch the live render pipeline.";
  }
  setVideoTutorStatus("Tutor video brief ready. Generate the live video next.", { visible: true });
  showToast("Tutor video brief ready.", "success");
}

function _videoTopicKey(topic, subject = "") {
  return `${String(topic || "").trim().toLowerCase()}::${String(subject || "").trim().toLowerCase()}`;
}

function _videoTopicSlug(topic) {
  return String(topic || "")
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "_")
    .replace(/^_+|_+$/g, "") || "topic";
}

function _inferVideoSubjectFromText(text) {
  const lower = String(text || "").toLowerCase();
  if (lower.includes("chem") || lower.includes("mole") || lower.includes("reaction") || lower.includes("bond") || lower.includes("equilibrium")) {
    return "Chemistry";
  }
  if (lower.includes("math") || lower.includes("integral") || lower.includes("derivative") || lower.includes("probability") || lower.includes("matrix") || lower.includes("geometry")) {
    return "Mathematics";
  }
  return "Physics";
}

function _inferVideoTopicFromText(text) {
  const lower = String(text || "").toLowerCase();
  const hints = [
    ["Projectile Motion", ["projectile", "trajectory", "parabola"]],
    ["Kinematics", ["kinematics", "motion in a straight line", "relative motion", "circular motion"]],
    ["Electrostatics", ["electrostatics", "electric field", "charge", "field lines"]],
    ["Current Electricity", ["current electricity", "ohm", "kirchhoff", "resistance"]],
    ["Chemical Equilibrium", ["equilibrium", "le chatelier", "kc", "kp"]],
    ["Mole Concept", ["mole", "stoichiometry", "limiting reagent"]],
    ["Differentiation", ["derivative", "differentiation", "tangent", "slope"]],
    ["Integration", ["integral", "integration", "area under curve"]],
    ["Probability", ["probability", "sample space", "event", "bayes"]],
    ["Matrices and Determinants", ["matrix", "determinant"]],
  ];
  for (const [topic, words] of hints) {
    if (words.some((word) => lower.includes(word))) {
      return topic;
    }
  }
  return String(text || "").trim().split(/\s+/).slice(0, 4).join(" ") || "the topic";
}

function updateAstraCurrentTopic(topic, subject, source) {
  window.astraCurrentTopic = {
    topic: topic ? String(topic).trim() : null,
    subject: subject ? String(subject).trim() : null,
    source: source ? String(source).trim() : null,
  };
  updateTutorInputTopicChip();
  renderVideoTutorCurrentTopic(window.astraCurrentTopic.topic, window.astraCurrentTopic.subject);
}

function _topicSubjectColor(subject) {
  const value = String(subject || "").toLowerCase();
  if (value.includes("chem")) {
    return "green";
  }
  if (value.includes("math")) {
    return "orange";
  }
  return "blue";
}

function _findBriefSection(brief, label) {
  if (!brief || !Array.isArray(brief.script_blocks)) {
    return "";
  }
  const found = brief.script_blocks.find((block) => String(block.label || "").toLowerCase() === String(label || "").toLowerCase());
  return (found && found.text) || "";
}

function renderSimpleVideoBrief(panel, brief) {
  if (!panel) {
    return;
  }
  panel.innerHTML = "";
  if (!brief) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = "The brief preview will appear here after you request a topic.";
    panel.appendChild(empty);
    return;
  }

  const header = document.createElement("div");
  header.className = "video-answer-brief-header";
  const titleBlock = document.createElement("div");
  const title = document.createElement("p");
  title.className = "card-title";
  title.textContent = `${brief.topic || "Video topic"} brief`;
  const meta = document.createElement("p");
  meta.className = "muted";
  meta.textContent = `${brief.subject || "JEE"} | ${brief.status || "brief_ready"} | ${brief.topic_slug || _videoTopicSlug(brief.topic || "")}`;
  titleBlock.appendChild(title);
  titleBlock.appendChild(meta);
  const status = document.createElement("span");
  status.className = "pill";
  status.textContent = brief.status || "brief_ready";
  header.appendChild(titleBlock);
  header.appendChild(status);
  panel.appendChild(header);

  const opening = document.createElement("p");
  opening.className = "muted";
  opening.textContent = _findBriefSection(brief, "Opening") || brief.question || "Opening will appear here.";
  panel.appendChild(opening);

  const concept = document.createElement("p");
  concept.className = "muted";
  concept.textContent = _findBriefSection(brief, "Concept") || brief.caption_text || "Explanation will appear here.";
  panel.appendChild(concept);

  const workedExample = document.createElement("p");
  workedExample.className = "muted";
  workedExample.textContent = _findBriefSection(brief, "Worked Example") || "Worked example will appear here.";
  panel.appendChild(workedExample);

  const recap = document.createElement("p");
  recap.className = "muted";
  recap.textContent = _findBriefSection(brief, "Recap") || brief.recap || "Recap will appear here.";
  panel.appendChild(recap);
}

function renderVideoTutorRequestedList(items) {
  if (!videoTutorRequestedList) {
    refreshVideoSearchResults();
    return;
  }
  videoTutorRequestedList.innerHTML = "";
  if (!Array.isArray(items) || !items.length) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = "Requested videos will appear here after you ask for a topic.";
    videoTutorRequestedList.appendChild(empty);
    return;
  }

  items.forEach((item) => {
    const card = document.createElement("div");
    card.className = "video-request-item";
    const head = document.createElement("div");
    const title = document.createElement("strong");
    title.textContent = item.topic || "Requested topic";
    const meta = document.createElement("p");
    meta.className = "muted";
    meta.textContent = `${item.subject || "JEE"} | ${item.status || "requested"}`;
    head.appendChild(title);
    head.appendChild(meta);

    const buttons = document.createElement("div");
    buttons.className = "mini-action-row";
    const watchBtn = document.createElement("button");
    watchBtn.type = "button";
    watchBtn.className = "ghost-button";
    watchBtn.textContent = "Watch";
    watchBtn.disabled = !item.video_url;
    watchBtn.addEventListener("click", () => {
      openGeneratedVideoForTopic(item.topic, item.subject, item.video_url || "");
    });
    buttons.appendChild(watchBtn);
    card.append(head, buttons);
    videoTutorRequestedList.appendChild(card);
  });
  refreshVideoSearchResults();
}

function renderVideoTutorWeeklyCards(items) {
  currentVideoTutorWeek = Array.isArray(items) ? items : [];
  renderVideoTutorSubjectItems(activeVideoSearchQuery);
}

function renderVideoTutorSuggestedChips(items) {
  if (!vtSuggestedChips) {
    return;
  }
  vtSuggestedChips.innerHTML = "";
  const topItems = (Array.isArray(items) ? items : [])
    .filter((item) => item && item.topic)
    .slice(0, 3);
  if (!topItems.length) {
    const chip = document.createElement("span");
    chip.className = "ghost-button";
    chip.textContent = "Ask for any topic";
    vtSuggestedChips.appendChild(chip);
    return;
  }
  topItems.forEach((item) => {
    const chip = document.createElement("button");
    chip.type = "button";
    chip.className = "ghost-button";
    chip.textContent = item.topic;
    chip.addEventListener("click", () => {
      if (videoQuestionInput) {
        videoQuestionInput.value = item.topic;
        videoQuestionInput.focus();
      }
      updateAstraCurrentTopic(item.topic, item.subject || _inferVideoSubjectFromText(item.topic), "weekly_plan");
    });
    vtSuggestedChips.appendChild(chip);
  });
}

function renderVideoTutorCurrentTopic(topic, subject) {
  const cleanTopic = String(topic || "").trim();
  const displaySubject = String(subject || "").trim();
  if (vtTopicName) {
    vtTopicName.textContent = cleanTopic || "-";
  }
  if (vtTopicSubject) {
    vtTopicSubject.textContent = displaySubject ? displaySubject : "";
  }
}

function _videoTutorActiveSubject() {
  return normalizeVideoSubject(activeVideoSubjectTab || "physics");
}

function _videoTutorTopicSubject(item) {
  return normalizeVideoSubject(item && (item.subject || item.topic || item.title || ""));
}

function _videoTutorMatchesActiveSubject(item, subject = activeVideoSubjectTab) {
  return _videoTutorTopicSubject(item) === normalizeVideoSubject(subject || "physics");
}

function _videoTutorSearchText(item) {
  return [
    item && item.title,
    item && item.topic,
    item && item.summary,
    item && item.description,
    item && item.status,
    item && item.subject,
  ]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();
}

function _videoTutorQueryMatches(item, query) {
  const cleanQuery = String(query || "").trim().toLowerCase();
  if (!cleanQuery) {
    return true;
  }
  const haystack = _videoTutorSearchText(item);
  return Boolean(haystack) && haystack.includes(cleanQuery);
}

function _videoTutorCombinedItems(subject = activeVideoSubjectTab, query = activeVideoSearchQuery) {
  const normalizedSubject = normalizeVideoSubject(subject || "physics");
  const cleanQuery = String(query || "").trim();
  const weeklyItems = Array.isArray(currentVideoTutorWeek) ? currentVideoTutorWeek : [];
  const libraryItems = Array.isArray(videoLibrarySnapshot && videoLibrarySnapshot.videos) ? videoLibrarySnapshot.videos : [];
  const requestedItems = Array.isArray(currentRequestedVideos) ? currentRequestedVideos : [];
  const seen = new Map();
  const merged = [];

  const addItem = (item, source) => {
    if (!item) {
      return;
    }
    const topic = String(item.topic || item.title || "").trim();
    if (!topic) {
      return;
    }
    const candidate = {
      ...item,
      topic,
      subject: item.subject || _inferVideoSubjectFromText(topic),
      _videoSource: source,
    };
    if (!_videoTutorMatchesActiveSubject(candidate, normalizedSubject)) {
      return;
    }
    if (cleanQuery && !_videoTutorQueryMatches(candidate, cleanQuery)) {
      return;
    }
    const key = _videoTopicSlug(candidate.topic || candidate.title || candidate.topic_slug || candidate.id || "");
    if (!key) {
      return;
    }
    if (seen.has(key)) {
      const existingIndex = seen.get(key);
      const existing = merged[existingIndex] || {};
      const mergedItem = {
        ...existing,
        ...candidate,
        _videoSource: existing._videoSource || candidate._videoSource || source,
      };
      merged[existingIndex] = mergedItem;
      return;
    }
    seen.set(key, merged.length);
    merged.push(candidate);
  };

  weeklyItems.forEach((item) => addItem(item, "weekly"));
  libraryItems.forEach((item) => addItem(item, "library"));
  requestedItems.forEach((item) => addItem(item, "requested"));
  return merged;
}

function _videoTutorItemBadge(item) {
  if (item && item.video_url) {
    return { text: "Available", className: "available" };
  }
  if (item && (item.script_ready || item.brief || String(item.status || "").toLowerCase().includes("script"))) {
    return { text: "Script Ready", className: "script" };
  }
  return { text: "Planned", className: "generate" };
}

function _videoTutorRenderItem(item) {
  const row = document.createElement("div");
  row.className = "video-request-item";

  const head = document.createElement("div");
  const title = document.createElement("strong");
  title.textContent = item.topic || item.title || "Video topic";
  const meta = document.createElement("p");
  meta.className = "muted";
  const subjectLabel = item.subject || _inferVideoSubjectFromText(item.topic || item.title || "");
  const sourceLabel = item._videoSource === "library" ? "Library" : item._videoSource === "requested" ? "Requested" : "Weekly";
  meta.textContent = [subjectLabel, item.day_label || "", sourceLabel].filter(Boolean).join(" | ");
  head.appendChild(title);
  head.appendChild(meta);

  const actions = document.createElement("div");
  actions.className = "mini-action-row";
  const badgeInfo = _videoTutorItemBadge(item);
  const badge = document.createElement("span");
  badge.className = `pill ${badgeInfo.className}`;
  badge.textContent = badgeInfo.text;
  actions.appendChild(badge);

  if (item.video_url) {
    const watchBtn = document.createElement("button");
    watchBtn.type = "button";
    watchBtn.className = "ghost-button";
    watchBtn.textContent = "Watch";
    watchBtn.addEventListener("click", () => {
      openGeneratedVideoForTopic(item.topic || item.title || "Video", item.subject || "", item.video_url || "");
    });
    actions.appendChild(watchBtn);
  } else {
    const generateBtn = document.createElement("button");
    generateBtn.type = "button";
    generateBtn.textContent = "Generate Video";
    generateBtn.addEventListener("click", () => {
      openVideoTutorTopic(item.topic || item.title || "Video", item.subject || "", item._videoSource || "weekly_plan");
    });
    actions.appendChild(generateBtn);
  }

  row.append(head, actions);
  row.addEventListener("click", (event) => {
    if (event.target && event.target.closest && event.target.closest("button")) {
      return;
    }
    if (item.video_url) {
      openGeneratedVideoForTopic(item.topic || item.title || "Video", item.subject || "", item.video_url || "");
      return;
    }
    if (item.script_ready || item.brief) {
      openVideoTutorTopic(item.topic || item.title || "Video", item.subject || "", item._videoSource || "weekly_plan");
      return;
    }
    if (videoTutorRequestTopicInput) {
      videoTutorRequestTopicInput.value = item.topic || item.title || "";
      videoTutorRequestTopicInput.focus();
    }
  });
  return row;
}

function renderVideoTutorSubjectItems(query = activeVideoSearchQuery) {
  if (!videoTutorWeeklyVideos) {
    return;
  }
  const subject = _videoTutorActiveSubject();
  const items = _videoTutorCombinedItems(subject, query);
  videoTutorWeeklyVideos.innerHTML = "";
  if (videoTutorWeeklyStatus) {
    const totalWeekly = (Array.isArray(currentVideoTutorWeek) ? currentVideoTutorWeek : [])
      .filter((item) => _videoTutorMatchesActiveSubject(item, subject)).length;
    const totalLibrary = (Array.isArray(videoLibrarySnapshot && videoLibrarySnapshot.videos) ? videoLibrarySnapshot.videos : [])
      .filter((item) => _videoTutorMatchesActiveSubject(item, subject)).length;
    const searchText = String(query || "").trim();
    videoTutorWeeklyStatus.textContent = searchText
      ? `Showing ${items.length} match${items.length === 1 ? "" : "es"} for ${subject}.`
      : `${totalWeekly} planned | ${totalLibrary} available | ${subject}`;
  }
  if (!items.length) {
    const empty = document.createElement("div");
    empty.className = "table-card";
    const text = document.createElement("p");
    text.className = "muted";
    text.textContent = String(query || "").trim()
      ? "No matching videos found for this subject yet."
      : "This subject will fill with your weekly videos and matching library clips.";
    empty.appendChild(text);
    videoTutorWeeklyVideos.appendChild(empty);
    return;
  }
  const [featuredItem, ...remainingItems] = items;
  if (featuredItem) {
    videoTutorWeeklyVideos.appendChild(_videoTutorRenderItem(featuredItem));
  }
  if (remainingItems.length) {
    const dropdown = document.createElement("details");
    dropdown.className = "video-week-dropdown";
    const summary = document.createElement("summary");
    summary.className = "video-week-dropdown-summary";
    summary.textContent = `More videos (${remainingItems.length})`;
    const list = document.createElement("div");
    list.className = "video-week-dropdown-list";
    remainingItems.forEach((item) => {
      const row = document.createElement("div");
      row.className = "video-week-dropdown-item";
      row.appendChild(_videoTutorRenderItem(item));
      list.appendChild(row);
    });
    dropdown.appendChild(summary);
    dropdown.appendChild(list);
    videoTutorWeeklyVideos.appendChild(dropdown);
  }
}

function switchVideoSubjectTab(subject = "physics") {
  const nextSubject = normalizeVideoSubject(subject || "physics");
  activeVideoSubjectTab = nextSubject;
  videoSubjectTabButtons.forEach((button) => {
    const isActive = normalizeVideoSubject(button.dataset.videoSubjectTab || "") === nextSubject;
    button.classList.toggle("active", isActive);
    button.setAttribute("aria-selected", String(isActive));
  });
  renderVideoTutorSubjectItems(activeVideoSearchQuery);
  scrollActivePanelToTop("videoTutorTab");
}

function _videoSearchNormalize(value) {
  return String(value || "").trim().toLowerCase();
}

function _videoSearchCanonicalSubject(value) {
  const normalized = _videoSearchNormalize(value);
  if (!normalized) {
    return "";
  }
  if (normalized.includes("chem")) {
    return "chemistry";
  }
  if (normalized.includes("math")) {
    return "mathematics";
  }
  if (normalized.includes("phys")) {
    return "physics";
  }
  return normalized;
}

function _videoSearchSubjectAllowed(itemSubject, selectedSubject) {
  const selected = _videoSearchCanonicalSubject(selectedSubject);
  if (!selected || selected === "all") {
    return true;
  }
  return _videoSearchCanonicalSubject(itemSubject || "") === selected;
}

function _videoSearchThumbnailNode(item) {
  const thumb = document.createElement("div");
  thumb.className = "vt-result-thumb";
  const imageUrl = item.thumbnail_url || item.poster_url || item.cover_url || item.image_url || item.thumbnail || item.poster || "";
  if (imageUrl) {
    const img = document.createElement("img");
    img.src = imageUrl;
    img.alt = item.topic || item.title || "Video";
    thumb.appendChild(img);
  } else if (item.video_url) {
    const video = document.createElement("video");
    video.src = item.video_url;
    video.muted = true;
    video.playsInline = true;
    video.preload = "metadata";
    thumb.appendChild(video);
  } else {
    thumb.textContent = String((item.topic || item.title || "V").slice(0, 1)).toUpperCase();
    thumb.classList.add("video-library-thumb-fallback");
  }
  return thumb;
}

function _videoSearchBadge(item) {
  if (item && item.video_url) {
    return { text: "Available", className: "available" };
  }
  const status = String(item && (item.status || item.brief_status || "") || "").toLowerCase();
  if (item && (item.script_ready || status.includes("brief") || status.includes("script") || item.brief)) {
    return { text: "Script Ready", className: "script" };
  }
  return { text: "New", className: "generate" };
}

function _videoSearchMatchScore(item, query) {
  const cleanQuery = _videoSearchNormalize(query);
  if (!cleanQuery) {
    return 1;
  }
  const haystack = [
    item && item.title,
    item && item.topic,
    item && item.summary,
    item && item.description,
    item && item.status,
    item && item.subject,
  ]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();
  if (!haystack) {
    return 0;
  }
  return haystack.includes(cleanQuery) ? 1 : 0;
}

function _videoSearchCandidateItems(query, subject) {
  const requested = Array.isArray(currentRequestedVideos) ? currentRequestedVideos : [];
  const library = Array.isArray(videoLibrarySnapshot && videoLibrarySnapshot.videos) ? videoLibrarySnapshot.videos : [];
  const mergeItems = [...requested, ...library];
  const deduped = [];
  const seen = new Set();
  mergeItems.forEach((item) => {
    if (!_videoSearchSubjectAllowed(item.subject || item.topic || "", subject)) {
      return;
    }
    if (!_videoSearchMatchScore(item, query)) {
      return;
    }
    const key = _videoTopicSlug(item.topic || item.title || item.topic_slug || item.id || "");
    if (!key || seen.has(key)) {
      return;
    }
    seen.add(key);
    deduped.push(item);
  });
  return deduped;
}

function _videoSearchDefaultItems(subject) {
  const requested = (Array.isArray(currentRequestedVideos) ? currentRequestedVideos : [])
    .slice(-3)
    .reverse();
  const library = (Array.isArray(videoLibrarySnapshot && videoLibrarySnapshot.videos) ? videoLibrarySnapshot.videos : [])
    .slice(-3)
    .reverse();
  const merged = [...requested];
  const seen = new Set(requested.map((item) => _videoTopicSlug(item.topic || item.title || item.topic_slug || item.id || "")));
  library.forEach((item) => {
    const key = _videoTopicSlug(item.topic || item.title || item.topic_slug || item.id || "");
    if (!seen.has(key)) {
      seen.add(key);
      merged.push(item);
    }
  });
  return merged;
}

function _videoSearchRenderItem(item, { generateNew = false } = {}) {
  const row = document.createElement("div");
  row.className = `vt-result-item${generateNew ? " generate-new" : ""}`;
  if (generateNew) {
    const info = document.createElement("div");
    info.className = "vt-result-info";
    const title = document.createElement("div");
    title.className = "vt-result-title";
    title.textContent = `+ Generate '${item || "topic"}' video`;
    const meta = document.createElement("div");
    meta.className = "vt-result-meta";
    meta.textContent = "Create a new brief and launch a fresh video pipeline.";
    info.appendChild(title);
    info.appendChild(meta);
    const badge = document.createElement("span");
    badge.className = "vt-result-badge generate";
    badge.textContent = "New";
    row.appendChild(info);
    row.appendChild(badge);
    row.addEventListener("click", () => {
      const topic = String(item || "").trim();
      if (!topic) {
        return;
      }
      if (videoTutorQuestionInput) {
        videoTutorQuestionInput.value = topic;
      }
      if (generateVideoAnswerBtn) {
        generateVideoAnswerBtn.click();
      } else {
        void generateVideoAnswerBrief();
      }
    });
    return row;
  }

  const thumb = _videoSearchThumbnailNode(item);
  const info = document.createElement("div");
  info.className = "vt-result-info";
  const title = document.createElement("div");
  title.className = "vt-result-title";
  title.textContent = item.topic || item.title || "Video topic";
  const meta = document.createElement("div");
  meta.className = "vt-result-meta";
  meta.textContent = [item.subject || "JEE", item.day_label || item.status || ""].filter(Boolean).join(" | ");
  info.appendChild(title);
  info.appendChild(meta);

  const badgeInfo = _videoSearchBadge(item);
  const badge = document.createElement("span");
  badge.className = `vt-result-badge ${badgeInfo.className}`;
  badge.textContent = badgeInfo.text;

  row.appendChild(thumb);
  row.appendChild(info);
  row.appendChild(badge);

  row.addEventListener("click", () => {
    if (item.video_url) {
      openGeneratedVideoForTopic(item.topic || item.title || "Video", item.subject || "", item.video_url);
      return;
    }
    if (badgeInfo.className === "script") {
      openVideoTutorTopic(item.topic || item.title || "Video", item.subject || "", item.source || "request");
      return;
    }
    if (videoTutorQuestionInput) {
      videoTutorQuestionInput.value = item.topic || item.title || "";
    }
    if (generateVideoAnswerBtn) {
      generateVideoAnswerBtn.click();
    } else {
      void generateVideoAnswerBrief();
    }
  });

  return row;
}

function renderVideoSearchResults(query = "", subject = activeVideoSubjectTab) {
  activeVideoSearchQuery = String(query || "").trim();
  activeVideoSubjectTab = normalizeVideoSubject(subject || activeVideoSubjectTab || "physics");
  renderVideoTutorSubjectItems(activeVideoSearchQuery);
}

function refreshVideoSearchResults() {
  renderVideoTutorSubjectItems(
    videoTutorRequestTopicInput ? videoTutorRequestTopicInput.value : activeVideoSearchQuery
  );
}

function initVideoSearch() {
  const input = videoTutorRequestTopicInput;
  const searchBar = document.querySelector(".vt-search-bar");
  if (!input || videoSearchBound) {
    return;
  }
  videoSearchBound = true;
  const rerender = () => renderVideoSearchResults(input.value, activeVideoSubjectTab);
  input.addEventListener("input", rerender);
  rerender();
  if (searchBar) {
    searchBar.dataset.bound = "1";
  }
}

function requestVideoForTopic() {
  const topic = String(videoTutorRequestTopicInput ? videoTutorRequestTopicInput.value : "").trim();
  const subject = activeVideoSubjectTab || "physics";
  const searchBar = document.querySelector(".vt-search-bar");
  if (!topic) {
    if (searchBar) {
      searchBar.classList.add("vt-shake");
      window.setTimeout(() => searchBar.classList.remove("vt-shake"), 380);
    }
    if (videoTutorRequestTopicInput) {
      videoTutorRequestTopicInput.focus();
    }
    return;
  }
  activeVideoSearchQuery = topic;
  updateAstraCurrentTopic(topic, normalizeVideoSubject(subject || _inferVideoSubjectFromText(topic)), "request");
  const combined = _videoTutorCombinedItems(subject, topic);
  const exactMatch = combined.find((item) => _videoTopicSlug(item.topic || item.title || "") === _videoTopicSlug(topic)) || null;

  if (exactMatch && exactMatch.video_url) {
    openGeneratedVideoForTopic(exactMatch.topic || topic, exactMatch.subject || subject, exactMatch.video_url);
    return;
  }
  if (exactMatch && (exactMatch.script_ready || exactMatch.brief || String(exactMatch.status || "").toLowerCase().includes("brief"))) {
    openVideoTutorTopic(exactMatch.topic || topic, exactMatch.subject || subject, exactMatch._videoSource || "weekly_plan");
    return;
  }
  if (videoTutorQuestionInput) {
    videoTutorQuestionInput.value = topic;
  }
  if (generateVideoAnswerBtn) {
    generateVideoAnswerBtn.click();
  } else {
    void generateVideoAnswerBrief();
  }
}

function setVideoTutorStatus(message, { visible = true } = {}) {
  if (videoRenderStatus) {
    videoRenderStatus.textContent = message || "";
  }
  if (videoStatusPanel) {
    videoStatusPanel.textContent = message || "";
    videoStatusPanel.classList.toggle("hidden", !visible);
  }
}

function buildVideoTutorWeekFromWeeklyPlan(weeklyPayload = {}, statusItems = []) {
  if (Array.isArray(statusItems) && statusItems.length) {
    return statusItems;
  }
  const built = [];
  (weeklyPayload.days || []).forEach((day) => {
    ["morning", "evening"].forEach((slot) => {
      const session = day && day[slot] ? day[slot] : null;
      if (!session || !session.topic) {
        return;
      }
      built.push({
        date: day.date || "",
        day_label: day.label || day.date || "",
        slot,
        subject: session.subject || "",
        topic: session.topic || "",
        topic_slug: _videoTopicSlug(session.topic),
        script_ready: false,
        video_ready: false,
        status: "Not prepared yet",
        brief: {},
        video_url: "",
        job_id: "",
      });
    });
  });
  return built;
}

async function loadVideoTutorWorkspace() {
  if (!activeProfile) {
    return;
  }
  if (videoTutorWeeklyStatus) {
    videoTutorWeeklyStatus.textContent = "Loading this week's video plan...";
  }
  try {
    const weeklyResponse = await fetch(`/api/planner/weekly/${encodeURIComponent(activeProfile.name)}`);
    const weeklyPayload = await weeklyResponse.json();

    try {
      await fetch("/api/video/pre-plan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ student_id: activeProfile.name, days_ahead: 7 }),
      });
    } catch (prePlanError) {
      console.warn("Could not pre-generate weekly video briefs:", prePlanError);
    }

    const [statusResponse, requestedResponse] = await Promise.all([
      fetch(`/api/video/pre-plan/status/${encodeURIComponent(activeProfile.name)}`),
      fetch(`/api/video/requests/${encodeURIComponent(activeProfile.name)}`),
    ]);
    const statusPayload = await statusResponse.json();
    const requestedPayload = await requestedResponse.json();
    currentVideoTutorPlanStatus = Array.isArray(statusPayload.items) ? statusPayload.items : [];
    currentRequestedVideos = Array.isArray(requestedPayload.requests) ? requestedPayload.requests : [];
    renderVideoTutorWeeklyCards(buildVideoTutorWeekFromWeeklyPlan(weeklyPayload || {}, currentVideoTutorPlanStatus));
    renderVideoTutorRequestedList(currentRequestedVideos);
    switchVideoSubjectTab(activeVideoSubjectTab || "physics");
    initVideoSearch();
    refreshVideoSearchResults();
    } catch (error) {
      if (videoTutorWeeklyStatus) {
        videoTutorWeeklyStatus.textContent = error.message || "Could not load the weekly video plan right now.";
      }
  }
}

async function saveRequestedVideo(topic, subject, source = "request", status = "requested", jobId = "", videoUrl = "") {
  if (!activeProfile || !topic) {
    return null;
  }
  try {
    const response = await fetch("/api/video/request", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        student_id: activeProfile.name,
        topic,
        subject,
        source,
        status,
        job_id: jobId,
        video_url: videoUrl,
      }),
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Could not save that video request.");
    }
    currentRequestedVideos = Array.isArray(payload.requests) ? payload.requests : currentRequestedVideos;
    renderVideoTutorRequestedList(currentRequestedVideos);
    return payload.request || null;
  } catch (error) {
    console.warn("Could not save requested video:", error);
    return null;
  }
}

async function updateRequestedVideoStatus(topicSlug, status, jobId = "", videoUrl = "") {
  if (!activeProfile || !topicSlug) {
    return null;
  }
  try {
    const response = await fetch("/api/video/request/status", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        student_id: activeProfile.name,
        topic: topicSlug,
        status,
        job_id: jobId,
        video_url: videoUrl,
      }),
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Could not update the requested video status.");
    }
    currentRequestedVideos = Array.isArray(payload.requests) ? payload.requests : currentRequestedVideos;
    renderVideoTutorRequestedList(currentRequestedVideos);
    return payload.request || null;
  } catch (error) {
    console.warn("Could not update requested video status:", error);
    return null;
  }
}

async function loadRequestedVideoBrief(topic, subject, source = "request") {
  if (!activeProfile || !topic) {
    return null;
  }
  const topicSlug = _videoTopicSlug(topic);
  activeVideoTutorRequest = { topic, subject, source, topic_slug: topicSlug };
  updateAstraCurrentTopic(topic, subject, source);
  if (videoTutorRequestStatus) {
    videoTutorRequestStatus.textContent = "Preparing the script preview...";
  }
  await saveRequestedVideo(topic, subject, source, "requested");
  try {
    const response = await fetch(`/api/video/brief/${encodeURIComponent(activeProfile.name)}/${encodeURIComponent(topicSlug)}?subject=${encodeURIComponent(subject || "")}`);
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Could not load the requested video brief.");
    }
    activeVideoTutorBrief = payload.brief || null;
    renderSimpleVideoBrief(videoTutorRequestBriefPanel, activeVideoTutorBrief);
    if (generateRequestedFullVideoBtn) {
      generateRequestedFullVideoBtn.disabled = false;
    }
    if (videoTutorRequestStatus) {
      videoTutorRequestStatus.textContent = `Brief ready for ${topic}.`;
    }
    setActiveStudioPane("lesson");
    return activeVideoTutorBrief;
  } catch (error) {
    if (videoTutorRequestBriefPanel) {
      videoTutorRequestBriefPanel.innerHTML = "";
      const note = document.createElement("p");
      note.className = "muted";
      note.textContent = error.message || "Could not load the requested brief right now.";
      videoTutorRequestBriefPanel.appendChild(note);
    }
    if (generateRequestedFullVideoBtn) {
      generateRequestedFullVideoBtn.disabled = true;
    }
    if (videoTutorRequestStatus) {
      videoTutorRequestStatus.textContent = error.message || "Could not load the requested brief right now.";
    }
    return null;
  }
}

function openVideoTutorTopic(topic, subject, source = "weekly_plan") {
  const cleanTopic = String(topic || "").trim();
  if (!cleanTopic) {
    return;
  }
  const nextSubject = normalizeVideoSubject(subject || _inferVideoSubjectFromText(cleanTopic));
  switchVideoSubjectTab(nextSubject);
  activeVideoSearchQuery = cleanTopic;
  updateAstraCurrentTopic(cleanTopic, nextSubject, source);
  if (videoTutorRequestTopicInput) {
    videoTutorRequestTopicInput.value = cleanTopic;
  }
  dismissedVideoSuggestionTopics.add(_videoTopicKey(cleanTopic, subject || ""));
  setActiveTab("videoTutorTab");
  void loadRequestedVideoBrief(cleanTopic, subject || _inferVideoSubjectFromText(cleanTopic), source);
}

function openGeneratedVideoForTopic(topic, subject, videoUrl = "") {
  const cleanTopic = String(topic || "").trim();
  if (cleanTopic) {
    const nextSubject = normalizeVideoSubject(subject || _inferVideoSubjectFromText(cleanTopic));
    switchVideoSubjectTab(nextSubject);
    activeVideoSearchQuery = cleanTopic;
    updateAstraCurrentTopic(cleanTopic, nextSubject, "request");
    if (videoTutorRequestTopicInput) {
      videoTutorRequestTopicInput.value = cleanTopic;
    }
  }
  setActiveTab("videoTutorTab");
  if (videoUrl) {
    if (tutorVideoPlayer) {
      tutorVideoPlayer.src = videoUrl;
      tutorVideoPlayer.classList.remove("hidden");
      tutorVideoPlayer.load();
      const playResult = tutorVideoPlayer.play();
      if (playResult && typeof playResult.catch === "function") {
        playResult.catch(() => {});
      }
    }
    if (videoTutorRequestStatus) {
      setVideoTutorStatus("Playing the generated video.", { visible: true });
    }
  }
}

function renderVideoSuggestionCard(topic, subject) {
  if (!chatFeed || !topic) {
    return;
  }
  const topicKey = _videoTopicKey(topic, subject);
  if (dismissedVideoSuggestionTopics.has(topicKey)) {
    return;
  }
  dismissedVideoSuggestionTopics.add(topicKey);
  const existing = chatFeed.querySelector(`.video-suggestion-card[data-topic-key="${CSS.escape(topicKey)}"]`);
  if (existing) {
    return;
  }
  const card = document.createElement("div");
  card.className = "video-suggestion-card";
  card.dataset.topicKey = topicKey;

  const text = document.createElement("p");
  text.className = "muted";
  text.textContent = `Want to watch a video explanation of ${topic}?`;

  const actions = document.createElement("div");
  actions.className = "mini-action-row";
  const watchBtn = document.createElement("button");
  watchBtn.type = "button";
  watchBtn.textContent = "Watch Video";
  watchBtn.addEventListener("click", () => {
    dismissedVideoSuggestionTopics.add(topicKey);
    openVideoTutorTopic(topic, subject || _inferVideoSubjectFromText(topic), "tutor");
    card.remove();
  });
  const dismissBtn = document.createElement("button");
  dismissBtn.type = "button";
  dismissBtn.className = "ghost-button";
  dismissBtn.textContent = "No thanks";
  dismissBtn.addEventListener("click", () => {
    dismissedVideoSuggestionTopics.add(topicKey);
    card.remove();
  });
  actions.appendChild(watchBtn);
  actions.appendChild(dismissBtn);
  card.appendChild(text);
  card.appendChild(actions);
  chatFeed.appendChild(card);
  syncTutorFullscreenOverlay();
}

async function generateVideoAnswerBrief() {
  if (!activeProfile) {
    return;
  }
  const question = (videoTutorQuestionInput && videoTutorQuestionInput.value.trim())
    || (lastTutorQuestion || (messageInput && messageInput.value) || lastTutorReply || "").trim();
  if (!question) {
    if (videoRenderStatus) {
      videoRenderStatus.textContent = "Ask Astra a question first, then generate the tutor video.";
      videoRenderStatus.style.display = "block";
    }
    setVideoTutorStatus("Ask Astra a question first, then generate the tutor video.", { visible: true });
    return;
  }

  const briefTopic = _inferVideoTopicFromText(question);
  const briefSubject = _inferVideoSubjectFromText(question);
  setAstraStatus(`Generating video for ${briefTopic}... scripting`, "working");
  logSessionActivity(`Requested video brief for ${briefTopic}`);

  if (generateVideoAnswerBtn) {
    generateVideoAnswerBtn.disabled = true;
    generateVideoAnswerBtn.textContent = "Generating...";
  }

  try {
    const topic = (lastVideoAnswerBrief && lastVideoAnswerBrief.topic) || question;
    const subject = (lastVideoAnswerBrief && lastVideoAnswerBrief.subject) || activeProfile.exam || "";
    const briefResponse = await fetch("/api/video-answer/brief", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        student_name: activeProfile.name,
        question,
        answer_text: lastTutorReply || "",
        conversation_mode: "tutor",
        tutor_level: Number(tutorLevelSelect && tutorLevelSelect.value) || 3,
      }),
    });
    const briefPayload = await briefResponse.json();
    if (!briefResponse.ok) {
      throw new Error(briefPayload.detail || "The video answer blueprint could not be created right now.");
    }
    if (briefPayload && briefPayload.video_answer_brief) {
      activeVideoTutorBrief = briefPayload.video_answer_brief;
      updateAstraCurrentTopic(
        briefPayload.video_answer_brief.topic || question,
        briefPayload.video_answer_brief.subject || _inferVideoSubjectFromText(question),
        "tutor"
      );
      renderVideoAnswerBrief(briefPayload.video_answer_brief);
      setActiveStudioPane("lesson");
      if (videoTutorQuestionInput) {
        videoTutorQuestionInput.value = question;
      }
    }
  } catch (error) {
    if (videoAnswerBriefPanel) {
      videoAnswerBriefPanel.innerHTML = "";
      const errorText = document.createElement("p");
      errorText.className = "muted";
      errorText.textContent = error.message || "The video answer could not be created right now.";
      videoAnswerBriefPanel.appendChild(errorText);
    }
  } finally {
    if (generateVideoAnswerBtn) {
      generateVideoAnswerBtn.disabled = false;
      generateVideoAnswerBtn.textContent = "Generate";
    }
    setAstraStatus(`Astra is ready. Today's focus: ${briefTopic} - ${briefSubject}`, "success", true);
    updateTutorRoomLivePanel();
  }
}

function normalizeVideoSubject(subject) {
  const value = String(subject || "").toLowerCase();
  if (value.includes("chem")) {
    return "chemistry";
  }
  if (value.includes("math")) {
    return "maths";
  }
  return "physics";
}

function inferVideoSubjectFromQuestion(question) {
  const text = String(question || "").toLowerCase();
  if (text.includes("chem") || text.includes("mole") || text.includes("reaction") || text.includes("bond")) {
    return "chemistry";
  }
  if (text.includes("math") || text.includes("integral") || text.includes("derivative") || text.includes("probability") || text.includes("calculus")) {
    return "maths";
  }
  return "physics";
}

function clearTutorVideoPolling() {
  if (activeTutorVideoPollInterval) {
    window.clearInterval(activeTutorVideoPollInterval);
    activeTutorVideoPollInterval = null;
  }
}

async function requestTutorVideo(question, topic, subject) {
  console.log("VIDEO ANSWER CLICKED - calling /api/video/generate");
  if (!activeProfile) {
    console.log("Video Answer aborted: no active profile.");
    return null;
  }

  const questionText = String(
    question
    || (videoTutorQuestionInput && videoTutorQuestionInput.value)
    || lastTutorQuestion
    || (messageInput && messageInput.value)
    || lastTutorReply
    || ""
  ).trim();
  if (!questionText) {
    console.log("Video Answer aborted: no question text.");
    setVideoTutorStatus("Ask Astra a tutor question first, then request the video answer.", { visible: true });
    return;
  }

  const activeTutorFace = activeAvatar || avatarPresets.find((avatar) => avatar.id === activeProfile.selected_avatar) || avatarPresets[0] || null;
  const tutorFaceUrl = (activeTutorFace && activeTutorFace.portrait_url) || (activeProfile && activeProfile.avatar_visuals && activeProfile.avatar_visuals.portrait_url) || "";
  const tutorPersonality = (activeProfile.tutor_style || activeProfile.tutor_personality_notes || activeTutorFace?.tagline || activeTutorFace?.name || "Warm, clear tutor").trim();
  const inferredTopic = String(topic || (lastVideoAnswerBrief && lastVideoAnswerBrief.topic) || questionText).trim();
  const inferredSubject = normalizeVideoSubject(subject || (lastVideoAnswerBrief && lastVideoAnswerBrief.subject) || inferVideoSubjectFromQuestion(questionText) || activeProfile.exam || "");
  updateAstraCurrentTopic(inferredTopic, inferredSubject, "request");
  setAstraStatus(`Generating video for ${inferredTopic}...`, "working");
  showKnowledgeBaseTag("", false);
  logSessionActivity(`Requested full video for ${inferredTopic}`);

  clearTutorVideoPolling();
  activeTutorVideoJobId = "";
  setVideoTutorStatus("Astra is preparing your explanation...", { visible: true });
  if (videoRenderStatus) {
    videoRenderStatus.textContent = "Astra is preparing your explanation...";
  }
  if (tutorVideoAnswerPlayer) {
    tutorVideoAnswerPlayer.classList.add("hidden");
    tutorVideoAnswerPlayer.removeAttribute("src");
    tutorVideoAnswerPlayer.load();
  }
  try {
    console.log("Video Answer request payload:", {
      student_id: activeProfile.name,
      question: questionText,
      topic: inferredTopic,
      subject: inferredSubject,
      tutor_face_url: tutorFaceUrl,
      tutor_personality: tutorPersonality,
    });
    const response = await fetch(`${videoApiBaseUrl}/api/video/generate`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({
        student_id: activeProfile.name,
        question: questionText,
        topic: inferredTopic,
        subject: inferredSubject,
        tutor_face_url: tutorFaceUrl,
        tutor_personality: tutorPersonality,
      }),
    });
    const payload = await response.json();
    console.log("Video Answer generate response:", payload);
    if (response.status === 401) {
      handleSessionExpired();
      return null;
    }
    if (!response.ok) {
      throw new Error(payload.detail || "Could not queue the tutor video request.");
    }
    activeTutorVideoJobId = payload.job_id || "";
    if (activeTutorVideoJobId) {
      startVideoPolling(activeTutorVideoJobId);
      if (topic) {
        void updateRequestedVideoStatus(_videoTopicSlug(topic), "generating", activeTutorVideoJobId, "");
      }
    } else {
      setVideoTutorStatus("The video job was queued, but no job id was returned.", { visible: true });
    }
    setAstraStatus(`Generating video for ${inferredTopic}... ${payload.job_id ? "queued" : "working"}`, "working");
    return activeTutorVideoJobId || null;
  } catch (error) {
    setVideoTutorStatus(error.message || "The video request could not be created right now.", { visible: true });
    if (videoRenderStatus) {
      videoRenderStatus.textContent = error.message || "The video request could not be created right now.";
    }
    setAstraStatus(`Could not generate video: ${error.message}`, "warning", true);
    updateTutorRoomLivePanel();
    return null;
  }
}

function onVideoReady(videoUrl, recapText = "") {
  clearTutorVideoPolling();
  activeTutorVideoJobId = "";
  if (tutorVideoAnswerPlayer) {
    tutorVideoAnswerPlayer.src = videoUrl;
    tutorVideoAnswerPlayer.classList.remove("hidden");
    tutorVideoAnswerPlayer.load();
    tutorVideoAnswerPlayer.onpause = () => {
      pauseTutorNarration();
      updateTutorRoomLivePanel();
    };
    tutorVideoAnswerPlayer.onplay = () => {
      resumeTutorNarration();
      updateTutorRoomLivePanel();
    };
    tutorVideoAnswerPlayer.onended = () => {
      updateTutorRoomLivePanel();
    };
    try {
      const playResult = tutorVideoAnswerPlayer.play();
      if (playResult && typeof playResult.catch === "function") {
        playResult.catch(() => {});
      }
    } catch (error) {
      // Ignore autoplay failures; controls remain available.
    }
  }
  setVideoTutorStatus("", { visible: false });
  if (videoTranscriptPanel) {
    videoTranscriptPanel.textContent = recapText || (lastVideoAnswerBrief && (lastVideoAnswerBrief.recap || lastVideoAnswerBrief.caption_text)) || "The tutor recap will appear here.";
  }
  if (videoRenderStatus) {
    videoRenderStatus.textContent = "Your tutor video is ready.";
  }
  if (activeVideoTutorRequest && activeVideoTutorRequest.topic) {
    void updateRequestedVideoStatus(
      activeVideoTutorRequest.topic_slug || _videoTopicSlug(activeVideoTutorRequest.topic),
      "ready",
      "",
      videoUrl || ""
    );
  }
  updateTutorRoomLivePanel();
}

function startVideoPolling(jobId) {
  if (!jobId) {
    return;
  }

  clearTutorVideoPolling();
  const statusMessages = {
    queued: "Astra is preparing your explanation...",
    generating_script: "Writing the teaching script...",
    generating_voice: "Recording the tutor voice...",
    rendering_video: "Generating your tutor video...",
    processing: "Generating your tutor video...",
    pending: "Generating your tutor video...",
  };

  const pollOnce = async () => {
    try {
      const response = await fetch(`${videoApiBaseUrl}/api/video/status/${encodeURIComponent(jobId)}`);
      const payload = await response.json();
      if (response.status === 401) {
        clearTutorVideoPolling();
        handleSessionExpired();
        return;
      }
      if (!response.ok) {
        throw new Error(payload.detail || "Could not read the tutor video status.");
      }
      const status = String(payload.status || "pending").toLowerCase();
      if (status === "ready" && payload.video_url) {
        onVideoReady(payload.video_url, payload.script?.recap || payload.script?.caption_text || "");
        setAstraStatus("Video ready. You can watch it now.", "success", true);
        return;
      }
      if (status === "failed") {
        clearTutorVideoPolling();
        setVideoTutorStatus("Something went wrong. Showing text answer instead.", { visible: true });
        if (videoRenderStatus) {
          videoRenderStatus.textContent = "Something went wrong. Showing text answer instead.";
        }
        if (tutorVideoAnswerPlayer) {
          tutorVideoAnswerPlayer.classList.add("hidden");
        }
        setAstraStatus("Video generation failed.", "warning", true);
        updateTutorRoomLivePanel();
        return;
      }
      setVideoTutorStatus(statusMessages[status] || "Astra is preparing your explanation...", { visible: true });
      if (videoRenderStatus) {
        videoRenderStatus.textContent = statusMessages[status] || "Astra is preparing your explanation...";
      }
      setAstraStatus(`Generating video for ${activeVideoTutorRequest?.topic || "your topic"}... ${String(statusMessages[status] || "Astra is preparing your explanation...").toLowerCase()}`, "working");
    } catch (error) {
      clearTutorVideoPolling();
      setVideoTutorStatus("Something went wrong. Showing text answer instead.", { visible: true });
      if (videoRenderStatus) {
        videoRenderStatus.textContent = error.message || "Something went wrong. Showing text answer instead.";
      }
      setAstraStatus(`Could not generate video: ${error.message}`, "warning", true);
      updateTutorRoomLivePanel();
    }
  };

  activeTutorVideoPollInterval = window.setInterval(pollOnce, 4000);
  pollOnce();
}

function buildLocalTutorBrain(profile, avatar, mode = "tutor") {
  const selectedAvatar = avatar || activeAvatar || avatarPresets[0] || null;
  const femaleMode = !selectedAvatar || ["calm-mentor", "friendly-senior"].includes(selectedAvatar.id);
  const level = Number((tutorLevelSelect && tutorLevelSelect.value) || (profile && profile.default_tutor_level) || 3);
  const avatarName = (selectedAvatar && selectedAvatar.name) || "Calm Mentor";
  const voiceStyle = femaleMode ? "warm, articulate, and easy to interrupt" : "clear and structured";
  return {
    brain_label: avatarName,
    mode,
    tutor_level: level,
    identity: femaleMode
      ? "Female tutor brain: warm, composed, and human-like."
      : `${avatarName} tutor brain: focused and supportive.`,
    tone: femaleMode ? "gentle, clear, and reassuring" : "clear and supportive",
    feel: femaleMode ? "warm and human-like" : "balanced and supportive",
    pressure: mode === "practice" ? "medium" : "medium",
    teaching_adjustment: femaleMode
      ? "Keep the explanation calm, human, and easy to interrupt."
      : "Keep the explanation small, clear, and check understanding before moving on.",
    next_step: "Start with the smallest useful action and grow from there.",
    voice_profile: {
      assistant_voice_family: femaleMode ? "female" : "neutral",
      speaking_style: voiceStyle,
    },
    resume_hint: "The student can interrupt at any point, then resume from the last useful checkpoint.",
  };
}

function renderMemory(memory) {
  if (!memorySummary) {
    return;
  }

  memorySummary.innerHTML = "";
  const sections = [
    { label: "People mentioned", items: (memory && memory.known_people) || [] },
    { label: "Interests and hobbies", items: (memory && memory.interests) || [] },
    { label: "Life notes", items: (memory && memory.life_notes) || [] },
    { label: "Recent check-ins", items: (((memory && memory.recent_checkins) || []).map((item) => item.note)) },
  ];

  const hasItems = sections.some((section) => section.items.length);
  if (!hasItems) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = "As you talk more, this space will gently remember what matters to you.";
    memorySummary.appendChild(empty);
    return;
  }

  sections.forEach((section) => {
    if (!section.items.length) {
      return;
    }
    const block = document.createElement("div");
    block.className = "memory-block";

    const heading = document.createElement("p");
    heading.className = "memory-heading";
    heading.textContent = section.label;
    block.appendChild(heading);

    section.items.slice(-4).forEach((item) => {
      const chip = document.createElement("span");
      chip.className = "memory-chip";
      chip.textContent = item;
      block.appendChild(chip);
    });

    memorySummary.appendChild(block);
  });
}

function renderStudentInsightsLegacy(payload) {
  if (!studentInsightSummary) {
    return;
  }

  const snapshot = payload && payload.insight_snapshot ? payload.insight_snapshot : payload || null;
  const architecture = payload && payload.architecture_snapshot ? payload.architecture_snapshot : snapshot?.architecture_snapshot || null;

  studentInsightSummary.innerHTML = "";
  if (!snapshot) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = "Your adaptive support snapshot will appear here.";
    studentInsightSummary.appendChild(empty);
    return;
  }

  const currentStateCard = document.createElement("div");
  currentStateCard.className = "insight-note-card";

  const stateTitle = document.createElement("p");
  stateTitle.className = "memory-heading";
  stateTitle.textContent = "Current state";

  const statRow = document.createElement("div");
  statRow.className = "insight-stat-row";
  [
    { label: "Emotional state", value: snapshot.emotional_state || "steady" },
    { label: "Sentiment trend", value: snapshot.sentiment_trend || "mixed" },
    { label: "Support style", value: snapshot.support_style || "balanced_support" },
    { label: "Academic risk", value: snapshot.academic_risk || "low" },
    { label: "Practice trend", value: snapshot.trend_signal || "building" },
  ].forEach((item) => {
    const chip = document.createElement("span");
    chip.className = "focus-pill";
    chip.textContent = `${item.label}: ${String(item.value).replace(/_/g, " ")}`;
    statRow.appendChild(chip);
  });
  currentStateCard.appendChild(stateTitle);
  currentStateCard.appendChild(statRow);
  studentInsightSummary.appendChild(currentStateCard);

  const nextActionCard = document.createElement("div");
  nextActionCard.className = "insight-note-card";

  const nextActionTitle = document.createElement("p");
  nextActionTitle.className = "memory-heading";
  nextActionTitle.textContent = "Next action";

  const nextActionText = document.createElement("p");
  nextActionText.className = "muted";
  nextActionText.textContent = (architecture && architecture.next_step)
    || snapshot.focus_recommendation
    || "Keep following the current rhythm and take the next small useful step.";

  nextActionCard.appendChild(nextActionTitle);
  nextActionCard.appendChild(nextActionText);

  if (snapshot.coach_note) {
    const coachNote = document.createElement("p");
    coachNote.className = "muted";
    coachNote.textContent = snapshot.coach_note;
    nextActionCard.appendChild(coachNote);
  }

  studentInsightSummary.appendChild(nextActionCard);

  if (architecture) {
    const arch = architecture;
    const architectureCard = document.createElement("div");
    architectureCard.className = "insight-note-card";

    const title = document.createElement("p");
    title.className = "memory-heading";
    title.textContent = "Astra architecture snapshot";

    const summary = document.createElement("p");
    summary.className = "muted";
    summary.textContent = arch.summary_line || "Astra is combining storage, behavior, progress, analytics, and route logic into one adaptive view.";

    const source = document.createElement("p");
    source.className = "muted";
    source.textContent = `Source pack: ${(arch.source_pack && arch.source_pack.label) || "Balanced source pack"} | Storage: ${arch.storage_backend || "local"} | Trend: ${(arch.analytics_trend || "building").replace(/_/g, " ")}`;

    const suggestion = document.createElement("p");
    suggestion.className = "architecture-suggestion";
    suggestion.textContent = arch.gentle_suggestion || "Optional suggestion: keep following the current rhythm and adjust only when needed.";

    architectureCard.appendChild(title);
    architectureCard.appendChild(summary);
    architectureCard.appendChild(source);
    architectureCard.appendChild(suggestion);
    studentInsightSummary.appendChild(architectureCard);
  }

  if (snapshot.focus_recommendation || snapshot.top_exam_focus || snapshot.top_mode_focus) {
    const trendCard = document.createElement("div");
    trendCard.className = "insight-note-card";

    const title = document.createElement("p");
    title.className = "memory-heading";
    title.textContent = "Why Astra is adjusting the plan";

    const note = document.createElement("p");
    note.className = "muted";
    note.textContent = snapshot.focus_recommendation || "Astra is balancing concept review and practice based on your recent activity.";

    trendCard.appendChild(title);
    trendCard.appendChild(note);

    if (snapshot.top_exam_focus || snapshot.top_mode_focus) {
      const detail = document.createElement("p");
      detail.className = "muted";
      detail.textContent = `Current pattern: ${snapshot.top_exam_focus || "general"} / ${snapshot.top_mode_focus || "general"}`;
      trendCard.appendChild(detail);
    }

    studentInsightSummary.appendChild(trendCard);
  }

  if ((snapshot.coaching_actions || []).length) {
    const actionCard = document.createElement("div");
    actionCard.className = "insight-note-card";

    const title = document.createElement("p");
    title.className = "memory-heading";
    title.textContent = "Support moves active in the background";
    actionCard.appendChild(title);

    (snapshot.coaching_actions || []).slice(0, 4).forEach((item) => {
      const line = document.createElement("p");
      line.className = "muted";
      line.textContent = `- ${item}`;
      actionCard.appendChild(line);
    });

    studentInsightSummary.appendChild(actionCard);
  }

  if ((snapshot.emotion_keywords || []).length) {
    const keywords = document.createElement("div");
    keywords.className = "insight-stat-row";
    snapshot.emotion_keywords.forEach((item) => {
      const chip = document.createElement("span");
      chip.className = "memory-chip";
      chip.textContent = item;
      keywords.appendChild(chip);
    });
    studentInsightSummary.appendChild(keywords);
  }
}

function renderStudentInsights(payload) {
  if (!studentInsightSummary) {
    return;
  }

  const snapshot = payload && payload.insight_snapshot ? payload.insight_snapshot : payload || null;
  const architecture = payload && payload.architecture_snapshot ? payload.architecture_snapshot : snapshot?.architecture_snapshot || null;

  studentInsightSummary.innerHTML = "";
  if (!snapshot) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = "Your adaptive support snapshot will appear here.";
    studentInsightSummary.appendChild(empty);
    return;
  }

  const currentStateCard = document.createElement("div");
  currentStateCard.className = "insight-note-card";

  const stateTitle = document.createElement("p");
  stateTitle.className = "memory-heading";
  stateTitle.textContent = "Current position";

  const statRow = document.createElement("div");
  statRow.className = "insight-stat-row";
  [
    { label: "State", value: snapshot.emotional_state || "steady" },
    { label: "Risk", value: snapshot.academic_risk || "low" },
    { label: "Trend", value: snapshot.trend_signal || "building" },
  ].forEach((item) => {
    const chip = document.createElement("span");
    chip.className = "focus-pill";
    chip.textContent = `${item.label}: ${String(item.value).replace(/_/g, " ")}`;
    statRow.appendChild(chip);
  });
  currentStateCard.appendChild(stateTitle);
  currentStateCard.appendChild(statRow);
  studentInsightSummary.appendChild(currentStateCard);

  const topicMemory = snapshot.topic_mastery || {};
  if (topicMemory.mastery_signal || (topicMemory.weak_topics && topicMemory.weak_topics.length) || (topicMemory.strong_topics && topicMemory.strong_topics.length)) {
    const memoryCard = document.createElement("div");
    memoryCard.className = "insight-note-card";

    const memoryTitle = document.createElement("p");
    memoryTitle.className = "memory-heading";
    memoryTitle.textContent = "Topic memory";
    memoryCard.appendChild(memoryTitle);

    const masteryLine = document.createElement("p");
    masteryLine.className = "muted";
    masteryLine.textContent = `Mastery signal: ${String(topicMemory.mastery_signal || "starting").replace(/_/g, " ")}`;
    memoryCard.appendChild(masteryLine);

    if (topicMemory.next_teaching_adjustment) {
      const adjustmentLine = document.createElement("p");
      adjustmentLine.className = "muted";
      adjustmentLine.textContent = topicMemory.next_teaching_adjustment;
      memoryCard.appendChild(adjustmentLine);
    }

    if (topicMemory.weak_topics && topicMemory.weak_topics.length) {
      const weakLine = document.createElement("p");
      weakLine.className = "muted";
      weakLine.textContent = `Weak topics: ${topicMemory.weak_topics.slice(0, 3).join(", ")}`;
      memoryCard.appendChild(weakLine);
    }

    if (topicMemory.strong_topics && topicMemory.strong_topics.length) {
      const strongLine = document.createElement("p");
      strongLine.className = "muted";
      strongLine.textContent = `Strong topics: ${topicMemory.strong_topics.slice(0, 3).join(", ")}`;
      memoryCard.appendChild(strongLine);
    }

    studentInsightSummary.appendChild(memoryCard);
  }

  const goalCard = document.createElement("div");
  goalCard.className = "insight-note-card";

  const goalTitle = document.createElement("p");
  goalTitle.className = "memory-heading";
  goalTitle.textContent = "Goal direction";

  const goalText = document.createElement("p");
  goalText.className = "muted";
  goalText.textContent = snapshot.focus_recommendation
    || (architecture && architecture.summary_line)
    || "Stay on the current path and keep building one small step at a time.";

  goalCard.appendChild(goalTitle);
  goalCard.appendChild(goalText);

  if (snapshot.top_exam_focus || snapshot.top_mode_focus) {
    const detail = document.createElement("p");
    detail.className = "muted";
    detail.textContent = `Main pattern: ${snapshot.top_exam_focus || "general"} / ${snapshot.top_mode_focus || "general"}`;
    goalCard.appendChild(detail);
  }

  if (snapshot.coach_note) {
    const coachNote = document.createElement("p");
    coachNote.className = "muted";
    coachNote.textContent = snapshot.coach_note;
    goalCard.appendChild(coachNote);
  }

  studentInsightSummary.appendChild(goalCard);

  const taskProfiles = snapshot.task_learning_profiles || {};
  const taskProfileList = Object.values(taskProfiles).sort((a, b) => {
    return (b.interactions || 0) - (a.interactions || 0);
  });
  if (taskProfileList.length) {
    const taskCard = document.createElement("div");
    taskCard.className = "insight-note-card";

    const title = document.createElement("p");
    title.className = "memory-heading";
    title.textContent = "Task learning signals";
    taskCard.appendChild(title);

    taskProfileList.slice(0, 3).forEach((item) => {
      const line = document.createElement("p");
      line.className = "muted";
      line.textContent = `${item.mode_label}: recent accuracy ${item.recent_accuracy || 0}% | trend ${String(item.trend_signal || "building").replace(/_/g, " ")} | ${item.adaptation || "Keep the current rhythm."}`;
      taskCard.appendChild(line);
    });

    studentInsightSummary.appendChild(taskCard);
  }

  if ((snapshot.coaching_actions || []).length) {
    const actionCard = document.createElement("div");
    actionCard.className = "insight-note-card";

    const title = document.createElement("p");
    title.className = "memory-heading";
    title.textContent = "Next steps";
    actionCard.appendChild(title);

    (snapshot.coaching_actions || []).slice(0, 3).forEach((item) => {
      const line = document.createElement("p");
      line.className = "muted";
      line.textContent = `- ${item}`;
      actionCard.appendChild(line);
    });

    studentInsightSummary.appendChild(actionCard);
  }
}

function renderEngagement(engagement) {
  const hasSidebarLeague = leagueName && leaguePoints && leagueNext && leagueRecent && leagueProgressFill && leagueMissions;
  const hasTabLeague = leagueTabName && leagueTabPoints && leagueTabStreak && leagueTabNext && leagueTabProgressFill && leagueTabLadder && leagueTabMissions && leagueTabRecent;
  const hasMiniLeague = miniLeagueTier && miniLeagueLP;
  if (!hasSidebarLeague && !hasTabLeague && !hasMiniLeague) {
    return;
  }

  if (!engagement) {
    if (hasMiniLeague) {
      miniLeagueTier.textContent = "Bronze 1";
      miniLeagueLP.textContent = "0 LP";
    }
    if (hasSidebarLeague) {
      leagueName.textContent = "Bronze 1";
      leaguePoints.textContent = "0 points collected so far.";
      leagueNext.textContent = "Next promotion will appear here.";
      leagueProgressFill.style.width = "0%";
      leagueMissions.innerHTML = '<p class="muted">Your quests will appear here.</p>';
      leagueRecent.innerHTML = '<p class="muted">Your latest point wins will appear here.</p>';
    }
    if (hasTabLeague) {
      leagueTabName.textContent = "Bronze 1";
      leagueTabPoints.textContent = "0";
      leagueTabStreak.textContent = "0 days";
      leagueTabNext.textContent = "Next promotion will appear here.";
      leagueTabProgressFill.style.width = "0%";
      leagueTabMissions.innerHTML = '<p class="muted">Your missions will appear here.</p>';
      leagueTabRecent.innerHTML = '<p class="muted">Your latest point wins will appear here.</p>';
      leagueTabLadder.innerHTML = "";
      LEAGUE_ORDER.forEach((leagueNameValue) => {
        const row = document.createElement("div");
        row.className = "league-ladder-row";
        row.innerHTML = `<span>${leagueNameValue}</span><span class="pill">Locked</span>`;
        leagueTabLadder.appendChild(row);
      });
    }
    return;
  }

  const currentLeague = engagement.current_league || "Bronze 1";
  const points = engagement.points || 0;
  const streak = engagement.current_streak || 0;
  const nextLeague = engagement.next_league;
  const pointsNeeded = engagement.points_needed_for_next || 0;
  const progressPercent = Math.max(0, Math.min(100, engagement.promotion_progress_percent || 0));
  const leagueIndex = Math.max(0, LEAGUE_ORDER.indexOf(currentLeague));

  if (hasMiniLeague) {
    miniLeagueTier.textContent = currentLeague;
    miniLeagueLP.textContent = `${points} LP`;
  }

  if (hasSidebarLeague) {
    leagueName.textContent = currentLeague;
    leaguePoints.textContent = `${points} points | Level ${engagement.level || 1} | ${streak}-day streak`;
    if (pointsNeeded > 0) {
      leagueNext.textContent = `${pointsNeeded} more points to reach ${nextLeague}.`;
    } else {
      leagueNext.textContent = "You are already at the highest available league right now.";
    }
    leagueProgressFill.style.width = `${progressPercent}%`;

    leagueMissions.innerHTML = "";
    const sidebarMissions = engagement.daily_missions || [];
    if (!sidebarMissions.length) {
      leagueMissions.innerHTML = '<p class="muted">Your quests will appear here.</p>';
    } else {
      sidebarMissions.slice(0, 4).forEach((mission) => {
        const row = document.createElement("div");
        row.className = `league-mission-card ${mission.status === "done" ? "mission-done" : "mission-active"}`;
        const title = document.createElement("p");
        title.className = "memory-heading";
        title.textContent = mission.title;
        const detail = document.createElement("p");
        detail.className = "muted";
        detail.textContent = mission.detail;
        row.appendChild(title);
        row.appendChild(detail);
        leagueMissions.appendChild(row);
      });
    }

    leagueRecent.innerHTML = "";
    const recentEvents = engagement.recent_events || [];
    if (!recentEvents.length) {
      leagueRecent.innerHTML = '<p class="muted">Your latest point wins will appear here.</p>';
    } else {
      recentEvents.slice(0, 5).forEach((item) => {
        const row = document.createElement("p");
        row.className = "muted";
        row.textContent = `+${item.points} points for ${item.reason}`;
        leagueRecent.appendChild(row);
      });
    }
  }
  if (hasTabLeague) {
    leagueTabName.textContent = currentLeague;
    leagueTabPoints.textContent = String(points);
    leagueTabStreak.textContent = `${streak} day${streak === 1 ? "" : "s"}`;
    leagueTabNext.textContent = pointsNeeded > 0
      ? `${pointsNeeded} more points to reach ${nextLeague}.`
      : "You are already at the highest available league right now.";
    leagueTabProgressFill.style.width = `${progressPercent}%`;

    leagueTabMissions.innerHTML = "";
    const tabMissions = engagement.daily_missions || [];
    if (!tabMissions.length) {
      leagueTabMissions.innerHTML = '<p class="muted">Your missions will appear here.</p>';
    } else {
      tabMissions.forEach((mission) => {
        const row = document.createElement("div");
        row.className = `league-mission-card ${mission.status === "done" ? "mission-done" : "mission-active"}`;

        const title = document.createElement("p");
        title.className = "memory-heading";
        title.textContent = mission.title;

        const detail = document.createElement("p");
        detail.className = "muted";
        detail.textContent = mission.detail;

        const footer = document.createElement("div");
        footer.className = "mission-footer";
        const status = document.createElement("span");
        status.className = `pill ${mission.status === "done" ? "done-pill" : "pending-pill"}`;
        status.textContent = mission.status === "done" ? `Done +${mission.reward}` : `Active +${mission.reward}`;
        footer.appendChild(status);

        row.appendChild(title);
        row.appendChild(detail);
        row.appendChild(footer);
        leagueTabMissions.appendChild(row);
      });
    }

    leagueTabRecent.innerHTML = "";
    const tabMilestones = engagement.recent_milestones || [];
    if (!tabMilestones.length) {
      leagueTabRecent.innerHTML = '<p class="muted">Finish tasks, revise topics, and log practice attempts to start climbing the leagues.</p>';
    } else {
      tabMilestones.slice().reverse().slice(0, 5).forEach((item) => {
        const row = document.createElement("p");
        row.className = "muted";
        row.textContent = `+${item.points} points for ${item.reason}`;
        leagueTabRecent.appendChild(row);
      });
    }

    leagueTabLadder.innerHTML = "";
    LEAGUE_ORDER.forEach((leagueNameValue, index) => {
      const row = document.createElement("div");
      const state = index < leagueIndex ? "complete" : index === leagueIndex ? "current" : "locked";
      row.className = `league-ladder-row league-${state}`;
      const label = document.createElement("span");
      label.textContent = leagueNameValue;
      const meta = document.createElement("span");
      meta.className = "pill";
      meta.textContent = state === "current" ? "Current" : state === "complete" ? "Cleared" : "Locked";
      row.appendChild(label);
      row.appendChild(meta);
      leagueTabLadder.appendChild(row);
    });
  }
}

async function fetchEngagement(studentName) {
  if (!studentName) {
    latestEngagementSnapshot = null;
    renderEngagement(null);
    return;
  }

  const previousTier = latestEngagementSnapshot && latestEngagementSnapshot.current_league;
  const response = await fetch(`/api/engagement/${encodeURIComponent(studentName)}`);
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || "Could not load league progress.");
  }
  latestEngagementSnapshot = payload.engagement || null;
  renderEngagement(latestEngagementSnapshot);
  const nextTier = latestEngagementSnapshot && latestEngagementSnapshot.current_league;
  if (previousTier && nextTier && previousTier !== nextTier) {
    showTierPromotion(previousTier, nextTier);
  }
}

function renderMemoryManager(memory) {
  if (!memoryManager) {
    return;
  }

  memoryManager.innerHTML = "";
  const sections = [
    { label: "Hobbies and interests", category: "interests", items: (memory && memory.interests) || [] },
    { label: "People you mentioned", category: "known_people", items: (memory && memory.known_people) || [] },
    { label: "Saved life notes", category: "life_notes", items: (memory && memory.life_notes) || [] },
  ];

  const hasItems = sections.some((section) => section.items.length);
  if (!hasItems) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = "Add hobbies or personal notes here, and remove old preferences whenever you want.";
    memoryManager.appendChild(empty);
    return;
  }

  sections.forEach((section) => {
    if (!section.items.length) {
      return;
    }

    const block = document.createElement("div");
    block.className = "manager-block";

    const heading = document.createElement("p");
    heading.className = "memory-heading";
    heading.textContent = section.label;
    block.appendChild(heading);

    const list = document.createElement("div");
    list.className = "manager-chip-list";

    section.items.forEach((item) => {
      const chip = document.createElement("div");
      chip.className = "editable-chip";

      const text = document.createElement("span");
      text.textContent = item;

      const removeButton = document.createElement("button");
      removeButton.type = "button";
      removeButton.className = "chip-remove";
      removeButton.textContent = "Remove";
      removeButton.addEventListener("click", () => removeMemoryItem(section.category, item));

      chip.appendChild(text);
      chip.appendChild(removeButton);
      list.appendChild(chip);
    });

    block.appendChild(list);
    memoryManager.appendChild(block);
  });
}

function normalizeExamEntry(exam) {
  const name = ((exam && exam.name) || "").trim();
  const examDate = ((exam && exam.exam_date) || "").trim();
  const subjects = Array.isArray(exam && exam.subjects)
    ? exam.subjects.map((subject) => String(subject).trim()).filter(Boolean)
    : String((exam && exam.subjects) || "")
        .split(",")
        .map((subject) => subject.trim())
        .filter(Boolean);
  const portion = ((exam && exam.portion) || "").trim();

  return {
    name,
    exam_date: examDate,
    subjects,
    portion,
  };
}

function renderExamManager(exams) {
  if (!examManager) {
    return;
  }

  examManager.innerHTML = "";
  if (!exams || !exams.length) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = "Add at least one exam so your plan can stay adaptive.";
    examManager.appendChild(empty);
    return;
  }

  exams.forEach((exam, index) => {
    const card = document.createElement("div");
    card.className = "exam-chip-card";

    const details = document.createElement("div");
    details.className = "exam-chip-copy";

    const title = document.createElement("p");
    title.className = "exam-chip-title";
    title.textContent = exam.name;

    const meta = document.createElement("p");
    meta.className = "muted";
    const portionText = exam.portion ? ` - Portion: ${exam.portion}` : "";
    meta.textContent = `${exam.exam_date} - ${((exam.subjects || []).join(", ")) || "Subjects pending"}${portionText}`;

    details.appendChild(title);
    details.appendChild(meta);

    const removeButton = document.createElement("button");
    removeButton.type = "button";
    removeButton.className = "ghost-button";
    removeButton.textContent = "Drop exam";
    removeButton.addEventListener("click", () => removeExamPlan(index));

    card.appendChild(details);
    card.appendChild(removeButton);
    examManager.appendChild(card);
  });
}

function getExamNameFromInputs() {
  if (examCatalogSelect && examCatalogSelect.value && examCatalogSelect.value !== "__custom__") {
    return examCatalogSelect.value.trim();
  }
  return (customExamNameInput && customExamNameInput.value.trim()) || "";
}

function updateExamInputMode() {
  if (!examCatalogSelect || !customExamNameInput || !examSubjectsInput) {
    return;
  }

  const selected = examCatalogSelect.value;
  const isCustom = selected === "__custom__";
  customExamNameInput.classList.toggle("hidden", !isCustom);

  if (!selected) {
    examSubjectsInput.value = "";
    examSubjectsInput.readOnly = false;
    return;
  }

  if (isCustom) {
    examSubjectsInput.readOnly = false;
    return;
  }

  const matchedExam = examCatalog.find((exam) => exam.name === selected);
  examSubjectsInput.value = matchedExam ? matchedExam.subjects.join(", ") : "";
  examSubjectsInput.readOnly = !!matchedExam;
}

function renderExamCatalogOptions() {
  if (!examCatalogSelect) {
    return;
  }

  const currentValue = examCatalogSelect.value;
  examCatalogSelect.innerHTML = `
    <option value="">Choose JEE Main or JEE Advanced</option>
    <option value="__custom__">My JEE track is not listed</option>
  `;
  examCatalog.forEach((exam) => {
    const option = document.createElement("option");
    option.value = exam.name;
    option.textContent = exam.name;
    examCatalogSelect.appendChild(option);
  });
  examCatalogSelect.value = currentValue || APP_CONFIG.default_exam || "JEE MAIN";
  updateExamInputMode();
}

function applyExplanationPreferences() {
  const textEnabled = showTextExplanation ? showTextExplanation.checked : true;
  const videoEnabled = showVideoExplanation ? showVideoExplanation.checked : false;
  const visualEnabled = showVisualExplanation ? showVisualExplanation.checked : false;
  if (chatFeed) {
    chatFeed.classList.toggle("text-hidden-mode", !textEnabled);
  }
  if (videoExplanationPanel) {
    videoExplanationPanel.classList.toggle("hidden", !videoEnabled);
  }
  if (visualLearningPanel) {
    visualLearningPanel.classList.toggle("hidden", !visualEnabled);
  }
  if (conceptCanvasPanel) {
    conceptCanvasPanel.classList.toggle("hidden", !visualEnabled);
  }
  if (reasoningPanel) {
    reasoningPanel.classList.toggle("hidden", !videoEnabled && !visualEnabled);
  }
}

function renderFunFact(funFact) {
  if (!funFactText || !funFactCategory) {
    return;
  }
  if (!funFact || !funFact.fact) {
    funFactText.textContent = "Your daily fun fact will appear here.";
    funFactCategory.textContent = "Today";
    return;
  }

  funFactText.textContent = funFact.fact;
  const label = funFact.category === "default" ? "General" : funFact.category;
  funFactCategory.textContent = label.charAt(0).toUpperCase() + label.slice(1);
}

function renderLearningSources(resources) {
  if (!learningSourcesList) {
    return;
  }

  learningSourcesList.innerHTML = "";
  if (!resources || !resources.length) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = "Add exams or subjects to unlock curated learning sources here.";
    learningSourcesList.appendChild(empty);
    return;
  }

  resources.forEach((resource) => {
    const card = document.createElement("a");
    card.className = "tips-resource-item assist-source-link";
    card.href = resource.url;
    card.target = "_blank";
    card.rel = "noreferrer noopener";

    const title = document.createElement("span");
    title.className = "exam-chip-title";
    title.textContent = resource.title || "Open source";

    const meta = document.createElement("span");
    meta.className = "muted";
    meta.textContent = [resource.source, resource.kind, resource.scope].filter(Boolean).join(" | ");

    card.appendChild(title);
    card.appendChild(meta);
    learningSourcesList.appendChild(card);
  });
}

function renderLearningSourcePack(pack) {
  if (learningSourcePackBadge) {
    learningSourcePackBadge.textContent = (pack && pack.label) || "Open Sources";
  }
}

function clearMockTestTimer() {
  if (activeMockTimerInterval) {
    window.clearInterval(activeMockTimerInterval);
    activeMockTimerInterval = null;
  }
}

function normalizeMockValue(value) {
  return String(value ?? "").trim().replace(/\s+/g, " ").toLowerCase();
}

function getMockAnswerKey(option, optionIndex) {
  const text = String(option || "").trim();
  const match = text.match(/^([A-D])[\).\s-]/i);
  return match ? match[1].toUpperCase() : String.fromCharCode(65 + optionIndex);
}

function formatMockAnswer(answer) {
  if (Array.isArray(answer)) {
    return answer.join(", ");
  }
  return String(answer || "");
}

function updateMockTimerLabel() {
  if (!mockTestTimer) {
    return;
  }
  if (!activeMockStartAt) {
    mockTestTimer.textContent = `${activeMockDurationMinutes || 60} min`;
    return;
  }
  const elapsedSeconds = Math.max(0, Math.floor((Date.now() - activeMockStartAt) / 1000));
  const totalSeconds = Math.max(60, Number(activeMockDurationMinutes || 60) * 60);
  const remaining = Math.max(0, totalSeconds - elapsedSeconds);
  const minutes = Math.floor(remaining / 60);
  const seconds = remaining % 60;
  mockTestTimer.textContent = `${minutes}:${String(seconds).padStart(2, "0")}`;
  if (remaining <= 0) {
    finishMockTest();
  }
}

function setMockPanelVisibility({ intro = true, question = false, report = false } = {}) {
  const sessionActive = !!(question || report);
  if (mockTestTab) {
    mockTestTab.classList.toggle("mock-session-active", sessionActive);
  }
  document.body.classList.toggle("mock-test-open", sessionActive);
  if (mockTestIntroCard) {
    mockTestIntroCard.classList.toggle("hidden", !intro);
  }
  if (mockTestQuestionCard) {
    mockTestQuestionCard.classList.toggle("hidden", !question);
  }
  if (mockTestReportCard) {
    mockTestReportCard.classList.toggle("hidden", !report);
  }
}

function exitMockTestRoom() {
  resetMockTestState();
  if (mockTestTab) {
    mockTestTab.classList.remove("mock-session-active");
  }
  document.body.classList.remove("mock-test-open");
  setActiveTab(lastNonMockTabId || "practiceTab");
}

function resetMockTestState() {
  clearMockTestTimer();
  activeMockTest = null;
  activeMockIndex = 0;
  activeMockAnswers = [];
  activeMockStartAt = null;
  activeMockDurationMinutes = 60;
  activeMockQuestionTimes = {};
  activeMockQuestionStartedAt = null;
  if (mockTestStatus) {
    mockTestStatus.textContent = "When you start, Astra will open one question at a time and then evaluate the full paper at the end.";
  }
  if (mockTestReportBody) {
    mockTestReportBody.innerHTML = "";
  }
  if (mockTestQuestionText) {
    mockTestQuestionText.textContent = "";
  }
  if (mockTestOptionList) {
    mockTestOptionList.innerHTML = "";
  }
  if (mockTestIntegerInput) {
    mockTestIntegerInput.value = "";
    mockTestIntegerInput.parentElement.classList.add("hidden");
  }
  setMockPanelVisibility({ intro: true, question: false, report: false });
  if (mockTestTab) {
    mockTestTab.classList.remove("mock-session-active");
  }
  document.body.classList.remove("mock-test-open");
  updateMockTimerLabel();
}

function recordCurrentMockQuestionTime() {
  if (!activeMockTest || !activeMockQuestionStartedAt) {
    return;
  }
  const question = activeMockTest.questions && activeMockTest.questions[activeMockIndex];
  if (!question || !question.id) {
    return;
  }
  const elapsed = Math.max(0, Math.round((Date.now() - activeMockQuestionStartedAt) / 1000));
  activeMockQuestionTimes[question.id] = (activeMockQuestionTimes[question.id] || 0) + elapsed;
  activeMockQuestionStartedAt = Date.now();
}

function renderMockQuestion() {
  if (!activeMockTest || !activeMockTest.questions || !activeMockTest.questions.length) {
    resetMockTestState();
    return;
  }

  const question = activeMockTest.questions[activeMockIndex];
  if (!question) {
    return;
  }

  setMockPanelVisibility({ intro: false, question: true, report: false });
  if (mockTestQuestionText) {
    mockTestQuestionText.textContent = question.question || "Question unavailable.";
  }
  if (mockTestProgress) {
    mockTestProgress.textContent = `${activeMockIndex + 1}/${activeMockTest.questions.length}`;
  }
  if (mockTestQuestionMeta) {
    mockTestQuestionMeta.textContent = `${question.unit || question.subject || "Physics"} - ${question.type || "mcq_single"} - ${question.difficulty || "medium"}`;
  }
  if (mockTestOptionList) {
    mockTestOptionList.innerHTML = "";
    const qType = String(question.type || "mcq_single");
    if (qType === "integer") {
      if (mockTestIntegerInput) {
        mockTestIntegerInput.parentElement.classList.remove("hidden");
        mockTestIntegerInput.value = activeMockAnswers[activeMockIndex] || "";
      }
    } else {
      if (mockTestIntegerInput) {
        mockTestIntegerInput.parentElement.classList.add("hidden");
      }
      const options = Array.isArray(question.options) ? question.options.slice(0, 4) : [];
      options.forEach((option, optionIndex) => {
        const answerKey = getMockAnswerKey(option, optionIndex);
        const currentAnswer = activeMockAnswers[activeMockIndex];
        const selected = qType === "mcq_multi"
          ? Array.isArray(currentAnswer) && currentAnswer.includes(answerKey)
          : normalizeMockValue(currentAnswer) === normalizeMockValue(answerKey);
        const button = document.createElement("button");
        button.type = "button";
        button.className = "mock-option";
        if (selected) {
          button.classList.add("selected");
        }
        button.textContent = option;
        button.addEventListener("click", () => {
          if (qType === "mcq_multi") {
            const existing = Array.isArray(activeMockAnswers[activeMockIndex]) ? activeMockAnswers[activeMockIndex].slice() : [];
            activeMockAnswers[activeMockIndex] = existing.includes(answerKey)
              ? existing.filter((item) => item !== answerKey)
              : existing.concat(answerKey).sort();
          } else {
            activeMockAnswers[activeMockIndex] = answerKey;
          }
          renderMockQuestion();
        });
        mockTestOptionList.appendChild(button);
      });
    }
  }
  if (mockTestNavPrev) {
    mockTestNavPrev.disabled = activeMockIndex === 0;
  }
  if (mockTestNavNext) {
    mockTestNavNext.textContent = activeMockIndex === activeMockTest.questions.length - 1 ? "Finish test" : "Next";
  }
  if (mockTestStatus) {
    mockTestStatus.textContent = "Choose the answer, move forward, and Astra will grade the full paper at the end.";
  }
  activeMockQuestionStartedAt = Date.now();
  updateMockTimerLabel();
}

async function loadMockCatalogue() {
  if (!activeProfile) {
    return;
  }
  if (mockCatalogueList) {
    mockCatalogueList.innerHTML = "<p class=\"muted\">Loading Physics mocks...</p>";
  }
  try {
    const response = await fetch("/api/mock/catalogue/physics");
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Could not load mock catalogue.");
    }
    mockCatalogue = Array.isArray(payload.mock_tests) ? payload.mock_tests : [];
    selectedMockTestId = selectedMockTestId || (mockCatalogue[0] && mockCatalogue[0].id) || "";
    renderMockCatalogue();
  } catch (error) {
    if (mockCatalogueList) {
      mockCatalogueList.innerHTML = `<p class="muted">${escapeHtml(error.message)}</p>`;
    }
  }
}

function renderMockCatalogue() {
  if (!mockCatalogueList) {
    return;
  }
  mockCatalogueList.innerHTML = "";
  if (!mockCatalogue.length) {
    mockCatalogueList.innerHTML = "<p class=\"muted\">No Physics mocks are available yet.</p>";
    return;
  }
  mockCatalogue.forEach((test) => {
    const card = document.createElement("div");
    card.className = "practice-mode-card";
    const title = document.createElement("h3");
    title.textContent = test.title || "Physics mock";
    const meta = document.createElement("p");
    meta.className = "muted";
    meta.textContent = `${test.total_questions || 0} questions - ${test.duration_minutes || 60} min - ${test.max_marks || 0} marks`;
    const topics = document.createElement("p");
    topics.className = "muted";
    topics.textContent = Array.isArray(test.topics_covered) ? test.topics_covered.join(", ") : "";
    const badge = document.createElement("span");
    badge.className = "pill";
    badge.textContent = test.difficulty || "medium";
    const button = document.createElement("button");
    button.type = "button";
    button.className = "ghost-button";
    button.textContent = "Start Test";
    button.addEventListener("click", () => {
      selectedMockTestId = test.id;
      startMockTest(test.id);
    });
    card.appendChild(title);
    card.appendChild(meta);
    card.appendChild(topics);
    card.appendChild(badge);
    card.appendChild(button);
    mockCatalogueList.appendChild(card);
  });
}

async function startMockTest(testId = "") {
  if (!activeProfile) {
    return;
  }

  const nextTestId = testId || selectedMockTestId || (mockCatalogue[0] && mockCatalogue[0].id) || "physics_mock_1";
  selectedMockTestId = nextTestId;
  setActiveTab("mockTestTab");
  if (mockTestStatus) {
    mockTestStatus.textContent = "Astra is loading your Physics mock...";
  }
  if (startMockTestBtn) {
    startMockTestBtn.disabled = true;
  }
  try {
    const response = await fetch(`/api/mock/test/${encodeURIComponent(nextTestId)}`);
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Could not create the mock test right now.");
    }
    activeMockTest = {
      ...(payload.test || {}),
      questions: Array.isArray(payload.questions) ? payload.questions : [],
    };
    activeMockIndex = 0;
    activeMockAnswers = new Array((activeMockTest.questions || []).length).fill("");
    activeMockQuestionTimes = {};
    activeMockQuestionStartedAt = Date.now();
    activeMockDurationMinutes = Number(activeMockTest.duration_minutes || activeMockTest.time_limit_minutes || 60);
    activeMockStartAt = Date.now();
    clearMockTestTimer();
    activeMockTimerInterval = window.setInterval(updateMockTimerLabel, 1000);
    setMockPanelVisibility({ intro: false, question: true, report: false });
    if (mockTestTab) {
      mockTestTab.scrollTop = 0;
    }
    renderMockQuestion();
  } catch (error) {
    if (mockTestStatus) {
      mockTestStatus.textContent = error.message;
    }
  } finally {
    if (startMockTestBtn) {
      startMockTestBtn.disabled = false;
    }
  }
}

function renderMockReport(report) {
  if (!mockTestReportBody) {
    return;
  }
  mockTestReportBody.innerHTML = "";

  const metrics = document.createElement("div");
  metrics.className = "mock-report-metrics";
  [
    { label: "Score", value: `${report.score}/${report.max_score}` },
    { label: "Accuracy", value: `${report.percentage}%` },
    { label: "Correct", value: `${report.correct}/${(report.question_review || []).length}` },
    { label: "Time taken", value: `${report.time_taken_minutes} min` },
  ].forEach((item) => {
    const card = document.createElement("div");
    card.className = "mock-metric-card";
    const label = document.createElement("p");
    label.className = "memory-heading";
    label.textContent = item.label;
    const value = document.createElement("strong");
    value.textContent = item.value;
    card.appendChild(label);
    card.appendChild(value);
    metrics.appendChild(card);
  });
  mockTestReportBody.appendChild(metrics);

  const topicBox = document.createElement("div");
  topicBox.className = "mock-metric-card";
  topicBox.innerHTML = `<p class="memory-heading">Topic breakdown</p>${Object.entries(report.topic_scores || {})
    .map(([topic, stats]) => `<p class="muted">${escapeHtml(topic)}: ${stats.percentage}% (${stats.score}/${stats.max})</p>`)
    .join("")}`;
  mockTestReportBody.appendChild(topicBox);

  const insight = document.createElement("div");
  insight.className = "mock-metric-card";
  const analysis = report.analysis || {};
  const actions = Array.isArray(analysis.top_3_actions) ? analysis.top_3_actions : [];
  insight.innerHTML = `<p class="memory-heading">Astra's read</p><p class="muted">${escapeHtml(analysis.overall_assessment || "Your baseline report will help Astra personalize planning and practice.")}</p><p class="muted">Weakest: ${escapeHtml(analysis.weakest_topic || "Review needed")} | Strongest: ${escapeHtml(analysis.strongest_topic || "Building")}</p><p class="muted">${escapeHtml(analysis.time_management || "")}</p>${actions.map((action) => `<p class="muted">- ${escapeHtml(action)}</p>`).join("")}`;
  mockTestReportBody.appendChild(insight);

  const reviewBox = document.createElement("div");
  reviewBox.className = "mock-metric-card";
  reviewBox.innerHTML = `<p class="memory-heading">Question review</p>${(report.question_review || []).map((item, index) => {
    const correct = item.type === "mcq_multi" ? (item.correct_options || []).join(", ") : (item.correct_answer || (item.correct_options || []).join(", "));
    return `<details><summary>Q${index + 1}: ${escapeHtml(item.status)} (${item.marks_awarded} marks)</summary><p class="muted">${escapeHtml(item.question)}</p><p class="muted">Your answer: ${escapeHtml(formatMockAnswer(item.student_answer) || "Skipped")} | Correct: ${escapeHtml(correct)}</p><p class="muted">${escapeHtml(item.solution || "")}</p></details>`;
  }).join("")}`;
  mockTestReportBody.appendChild(reviewBox);

  setMockPanelVisibility({ intro: false, question: false, report: true });
}

async function finishMockTest() {
  if (!activeMockTest || !activeMockTest.questions || !activeMockTest.questions.length || !activeProfile) {
    return;
  }
  saveCurrentMockAnswer();
  recordCurrentMockQuestionTime();
  clearMockTestTimer();
  const answers = {};
  activeMockTest.questions.forEach((question, index) => {
    if (activeMockAnswers[index] !== "" && activeMockAnswers[index] !== null && activeMockAnswers[index] !== undefined) {
      answers[question.id] = activeMockAnswers[index];
    }
  });
  const timeTaken = Math.max(1, Math.round((Date.now() - (activeMockStartAt || Date.now())) / 60000));
  if (mockTestStatus) {
    mockTestStatus.textContent = "Astra is grading your paper...";
  }
  try {
    const response = await fetch(`/api/mock/submit/${encodeURIComponent(activeMockTest.id || selectedMockTestId)}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        student_id: activeProfile.name,
        answers,
        time_taken_minutes: timeTaken,
        question_times: activeMockQuestionTimes,
      }),
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Could not submit the mock test.");
    }
    payload.time_taken_minutes = timeTaken;
    setActiveTab("mockTestTab");
    renderMockReport(payload);
    await refreshEngagementAfterLPAward(payload.lp_awards);
    if (mockTestStatus) {
      mockTestStatus.textContent = `Mock complete. Score ${payload.score}/${payload.max_score} (${payload.percentage}%).`;
    }
    await loadMockHistory();
    await fetchStudentInsights(activeProfile.name);
    await fetchStorageStatus(activeProfile.name);
  } catch (error) {
    if (mockTestStatus) {
      mockTestStatus.textContent = error.message;
    }
  }
}

function saveCurrentMockAnswer() {
  if (!activeMockTest || !activeMockTest.questions || !activeMockTest.questions.length) {
    return;
  }
  const question = activeMockTest.questions[activeMockIndex];
  if (!question) {
    return;
  }
  if ((question.type || "mcq") === "integer") {
    activeMockAnswers[activeMockIndex] = mockTestIntegerInput ? mockTestIntegerInput.value.trim() : "";
  }
}

function goToMockQuestion(direction) {
  if (!activeMockTest || !activeMockTest.questions || !activeMockTest.questions.length) {
    return;
  }
  saveCurrentMockAnswer();
  recordCurrentMockQuestionTime();
  const nextIndex = activeMockIndex + direction;
  if (nextIndex >= activeMockTest.questions.length) {
    finishMockTest();
    return;
  }
  if (nextIndex < 0) {
    return;
  }
  activeMockIndex = nextIndex;
  renderMockQuestion();
}

async function analyseExternalMock() {
  if (!activeProfile) {
    return;
  }
  const payload = {
    student_id: activeProfile.name,
    exam_type: mockExternalExamType ? mockExternalExamType.value : "JEE Main",
    total_score: Number(mockExternalTotalScore && mockExternalTotalScore.value),
    max_score: Number(mockExternalMaxScore && mockExternalMaxScore.value),
    physics_score: mockExternalPhysicsScore && mockExternalPhysicsScore.value ? Number(mockExternalPhysicsScore.value) : null,
    chemistry_score: mockExternalChemistryScore && mockExternalChemistryScore.value ? Number(mockExternalChemistryScore.value) : null,
    maths_score: mockExternalMathsScore && mockExternalMathsScore.value ? Number(mockExternalMathsScore.value) : null,
    time_taken: Number(mockExternalTimeTaken && mockExternalTimeTaken.value) || 0,
    notes: mockExternalNotes ? mockExternalNotes.value.trim() : "",
  };
  if (!Number.isFinite(payload.total_score) || !Number.isFinite(payload.max_score) || payload.max_score <= 0) {
    if (mockExternalAnalysisResult) {
      mockExternalAnalysisResult.innerHTML = "<p class=\"muted\">Enter total score and max marks first.</p>";
    }
    return;
  }
  if (mockExternalAnalyseBtn) {
    mockExternalAnalyseBtn.disabled = true;
  }
  try {
    const response = await fetch("/api/mock/analyse-external", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const result = await response.json();
    if (!response.ok) {
      throw new Error(result.detail || "Could not analyse this mock.");
    }
    renderExternalMockAnalysis(result);
    await refreshEngagementAfterLPAward(result.lp_awards);
    await loadMockHistory();
  } catch (error) {
    if (mockExternalAnalysisResult) {
      mockExternalAnalysisResult.innerHTML = `<p class="muted">${escapeHtml(error.message)}</p>`;
    }
  } finally {
    if (mockExternalAnalyseBtn) {
      mockExternalAnalyseBtn.disabled = false;
    }
  }
}

function renderExternalMockAnalysis(result) {
  if (!mockExternalAnalysisResult) {
    return;
  }
  const analysis = result.analysis || {};
  const actions = Array.isArray(analysis.top_3_actions) ? analysis.top_3_actions : [];
  mockExternalAnalysisResult.innerHTML = `<div class="mock-metric-card"><p class="memory-heading">Astra's analysis</p><p class="muted">Score: ${escapeHtml(result.percentage)}%</p><p class="muted">${escapeHtml(analysis.overall_assessment || "")}</p><p class="muted">Next focus: ${escapeHtml(analysis.next_week_focus || analysis.weakest_topic || "Targeted revision")}</p>${actions.map((action) => `<p class="muted">- ${escapeHtml(action)}</p>`).join("")}</div>`;
}

async function loadMockHistory() {
  if (!activeProfile || !mockHistoryList) {
    return;
  }
  mockHistoryList.innerHTML = "<p class=\"muted\">Loading recent tests...</p>";
  try {
    const response = await fetch(`/api/mock/history/${encodeURIComponent(activeProfile.name)}`);
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Could not load mock history.");
    }
    renderMockHistory((payload.results || []).slice(0, 5));
  } catch (error) {
    mockHistoryList.innerHTML = `<p class="muted">${escapeHtml(error.message)}</p>`;
  }
}

function renderMockHistory(results) {
  if (!mockHistoryList) {
    return;
  }
  mockHistoryList.innerHTML = "";
  if (!results.length) {
    mockHistoryList.innerHTML = "<p class=\"muted\">No mock tests saved yet.</p>";
    return;
  }
  results.forEach((item) => {
    const percentage = Number(item.percentage || 0);
    const color = percentage > 70 ? "#42d392" : percentage >= 50 ? "#ffd166" : "#ff6b6b";
    const details = document.createElement("details");
    details.className = "mock-metric-card";
    const summary = document.createElement("summary");
    summary.innerHTML = `${escapeHtml(item.taken_at || "")} - ${escapeHtml(item.exam_type || "Mock test")} <span class="pill" style="border-color:${color};color:${color}">${percentage}%</span>`;
    const analysis = item.analysis && (item.analysis.analysis || item.analysis) || {};
    const body = document.createElement("div");
    body.innerHTML = `<p class="muted">Score: ${escapeHtml(item.total_score)}/${escapeHtml(item.max_score)}</p><p class="muted">${escapeHtml(analysis.overall_assessment || "")}</p><p class="muted">Next focus: ${escapeHtml(analysis.next_week_focus || analysis.weakest_topic || "")}</p>`;
    details.appendChild(summary);
    details.appendChild(body);
    mockHistoryList.appendChild(details);
  });
}

function renderStudyGroupMessage(container, message, currentUserId) {
  if (!container || !message) {
    return;
  }
  const bubble = document.createElement("div");
  const isStudent = message.sender_type === "student";
  const isOwn = isStudent && message.sender_id === currentUserId;
  bubble.className = `message ${isStudent ? "student" : "tutor"}${isOwn ? " own-group-message" : ""}`;
  const label = document.createElement("p");
  label.className = "group-message-label";
  label.textContent = isStudent ? (isOwn ? "You" : message.sender_id || "Student") : "Classroom tutor";
  const body = document.createElement("p");
  body.textContent = message.content || "";
  bubble.appendChild(label);
  bubble.appendChild(body);
  container.appendChild(bubble);
}

function renderStudyGroupFeed(container, messages, emptyText) {
  if (!container) {
    return;
  }
  container.innerHTML = "";
  if (!messages || !messages.length) {
    const empty = document.createElement("div");
    empty.className = "message tutor";
    empty.innerHTML = `<p>${escapeHtml(emptyText)}</p>`;
    container.appendChild(empty);
    return;
  }
  messages.forEach((message) => renderStudyGroupMessage(container, message, activeProfile && activeProfile.name));
  container.scrollTop = container.scrollHeight;
}

function renderActiveGroupSession(session) {
  activeGroupSession = session || null;
  if (activeGroupSessionPill) {
    activeGroupSessionPill.textContent = session ? session.status || "scheduled" : "None";
  }
  if (!activeGroupSessionCard) {
    return;
  }
  activeGroupSessionCard.innerHTML = "";
  if (!session) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = "No active group session yet.";
    activeGroupSessionCard.appendChild(empty);
    return;
  }
  const title = document.createElement("p");
  title.className = "exam-chip-title";
  title.textContent = session.topic || "Group session";
  const meta = document.createElement("p");
  meta.className = "muted";
  meta.textContent = `${session.exam || "JEE"} | ${session.pace_band || "steady"} pace | ${session.member_count || 0}/3 students`;
  const members = document.createElement("div");
  members.className = "manager-chip-list";
  (session.members || []).forEach((member) => {
    const chip = document.createElement("span");
    chip.className = "memory-chip";
    chip.textContent = `${member.label || member.user_id}${member.status === "in_breakout" ? " - breakout" : ""}`;
    members.appendChild(chip);
  });
  const button = document.createElement("button");
  button.type = "button";
  button.className = "ghost-button";
  button.textContent = session.status === "scheduled" ? "Join session" : "Open session";
  button.addEventListener("click", () => openGroupSession(session));
  activeGroupSessionCard.appendChild(title);
  activeGroupSessionCard.appendChild(meta);
  activeGroupSessionCard.appendChild(members);
  activeGroupSessionCard.appendChild(button);
}

function renderGroupCandidateCard(group) {
  const card = document.createElement("div");
  card.className = "study-group-option-card";
  const title = document.createElement("p");
  title.className = "exam-chip-title";
  title.textContent = group.topic || "Pending topic";
  const meta = document.createElement("p");
  meta.className = "muted";
  meta.textContent = `${group.exam || "JEE"} | ${group.pace_band || "steady"} pace | ${group.member_count || 1}/3 students`;
  const members = document.createElement("div");
  members.className = "manager-chip-list";
  (group.members || []).slice(0, 3).forEach((member) => {
    const chip = document.createElement("span");
    chip.className = "memory-chip";
    chip.textContent = member.label || member.user_id || "Student";
    members.appendChild(chip);
  });
  const button = document.createElement("button");
  button.type = "button";
  button.textContent = "Join";
  button.addEventListener("click", () => joinStudyGroup(group));
  card.appendChild(title);
  card.appendChild(meta);
  card.appendChild(members);
  card.appendChild(button);
  return card;
}

function renderStudyGroups(payload) {
  const activeSession = payload && payload.active_session;
  renderActiveGroupSession(activeSession || null);
  if (studyGroupsStatus) {
    if (payload && payload.next_topic) {
      studyGroupsStatus.textContent = `Next pending topic: ${payload.next_topic.topic || "topic"}. Pace band: ${payload.pace_band || "steady"}.`;
    } else {
      studyGroupsStatus.textContent = "Add a pending topic in Progress so Astra can match a group class.";
    }
  }
  if (groupCandidatesList) {
    groupCandidatesList.innerHTML = "";
    const groups = (payload && payload.groups) || [];
    if (!groups.length) {
      const empty = document.createElement("p");
      empty.className = "muted";
      empty.textContent = "No group options are ready yet.";
      groupCandidatesList.appendChild(empty);
    } else {
      groups.forEach((group) => groupCandidatesList.appendChild(renderGroupCandidateCard(group)));
    }
  }
  if (activeSession && activeSession.main_messages) {
    openGroupSession(activeSession, { silent: true });
  }
}

function openGroupSession(session, options = {}) {
  if (!session) {
    return;
  }
  activeGroupSession = session;
  if (groupSessionPanel) {
    groupSessionPanel.classList.remove("hidden");
  }
  if (groupSessionTitle) {
    groupSessionTitle.textContent = session.topic || "Group session";
  }
  if (groupSessionMeta) {
    groupSessionMeta.textContent = `${session.subject || "Subject"} | ${session.exam || "JEE"} | ${session.pace_band || "steady"} pace | ${session.member_count || 0}/3 students`;
  }
  renderStudyGroupFeed(groupMainFeed, session.main_messages || [], "The group class feed will appear here.");
  renderStudyGroupFeed(groupBreakoutFeed, session.breakout_messages || [], "Step out when you need a private clarification.");
  if (groupBreakoutPanel) {
    groupBreakoutPanel.classList.toggle("hidden", session.current_user_status !== "in_breakout");
  }
  if (!options.silent && groupSessionPanel) {
    groupSessionPanel.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

async function refreshActiveGroupMessages() {
  if (!activeProfile || !activeGroupSession || !activeGroupSession.id) {
    return;
  }
  const response = await fetch(`/api/group-sessions/${encodeURIComponent(activeGroupSession.id)}/messages?user_id=${encodeURIComponent(activeProfile.name)}`);
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || "Could not load group messages.");
  }
  activeGroupSession = { ...(payload.session || activeGroupSession), main_messages: payload.main_messages || [], breakout_messages: payload.breakout_messages || [] };
  openGroupSession(activeGroupSession, { silent: true });
}
function createProgressItemCard(item) {
  const card = document.createElement("div");
  card.className = "progress-item-card";

  const top = document.createElement("div");
  top.className = "progress-item-top";

  const copy = document.createElement("div");
  const topic = document.createElement("p");
  topic.className = "progress-topic";
  topic.textContent = item.topic || "Untitled topic";

  const meta = document.createElement("p");
  meta.className = "progress-meta";
  const examBits = [item.exam, item.subject].filter(Boolean);
  meta.textContent = examBits.length ? examBits.join(" - ") : "General progress item";

  copy.appendChild(topic);
  copy.appendChild(meta);

  const pill = document.createElement("span");
  pill.className = `pill progress-pill ${item.status}-pill`;
  pill.textContent = item.status === "done" ? "Done" : item.status === "revise" ? "Revise" : "Pending";

  top.appendChild(copy);
  top.appendChild(pill);
  card.appendChild(top);

  if (item.note) {
    const note = document.createElement("p");
    note.className = "muted";
    note.textContent = item.note;
    card.appendChild(note);
  }

  const actions = document.createElement("div");
  actions.className = "progress-actions";
  [
    { status: "done", label: "Green tick" },
    { status: "revise", label: "Brown mark" },
    { status: "pending", label: "Red mark" },
  ].forEach((option) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "progress-mini";
    button.textContent = option.label;
    button.dataset.progressId = item.id;
    button.dataset.progressStatus = option.status;
    actions.appendChild(button);
  });
  card.appendChild(actions);
  return card;
}

function renderProgressColumn(target, items, emptyText) {
  if (!target) {
    return;
  }
  target.innerHTML = "";
  if (!items || !items.length) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = emptyText;
    target.appendChild(empty);
    return;
  }
  items.forEach((item) => target.appendChild(createProgressItemCard(item)));
}

function createChapterStatusCard(chapter) {
  const card = document.createElement("div");
  card.className = "progress-item-card";

  const top = document.createElement("div");
  top.className = "progress-item-top";

  const copy = document.createElement("div");
  const title = document.createElement("p");
  title.className = "progress-topic";
  title.textContent = chapter.chapter_name || chapter.unit_name || "Untitled chapter";

  const meta = document.createElement("p");
  meta.className = "progress-meta";
  meta.textContent = chapter.subject || "General";

  copy.append(title, meta);

  const score = chapter.chapter_test_score;
  const scorePill = document.createElement("span");
  scorePill.className = "pill";
  scorePill.textContent = score !== null && score !== undefined ? `${Math.round(Number(score) || 0)}%` : "No score";

  top.append(copy, scorePill);
  card.appendChild(top);

  const lastStudied = chapter.last_studied || chapter.completed_date || chapter.updated_at || "";
  const details = document.createElement("p");
  details.className = "muted";
  details.textContent = `Last studied: ${lastStudied ? String(lastStudied).slice(0, 10) : "-"}`;
  card.appendChild(details);

  return card;
}

function renderChapterStatusColumn(target, chapters) {
  if (!target) {
    return;
  }
  target.innerHTML = "";
  if (!chapters || !chapters.length) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = "Complete your first session to see topics appear here";
    target.appendChild(empty);
    return;
  }
  chapters.forEach((chapter) => target.appendChild(createChapterStatusCard(chapter)));
}

function renderProgressStatusFromChapterMastery(payload) {
  const chapters = Array.isArray(payload && payload.chapters) ? payload.chapters : [];
  const done = [];
  const revise = [];
  const pending = [];
  chapters.forEach((chapter) => {
    const scoreValue = chapter.chapter_test_score;
    const hasScore = scoreValue !== null && scoreValue !== undefined && scoreValue !== "";
    const score = hasScore ? Number(scoreValue) : null;
    const level = String(chapter.mastery_level || chapter.status || "").trim().toLowerCase();
    const status = String(chapter.status || "").trim().toLowerCase();
    if ((level === "mastered" || status === "mastered" || (score !== null && score >= 85))) {
      done.push(chapter);
    } else if (status === "not_started" || level === "not_started" || score === null || score < 50) {
      pending.push(chapter);
    } else if (["proficient", "developing"].includes(level) || ["proficient", "developing"].includes(status) || (score >= 50 && score <= 84)) {
      revise.push(chapter);
    } else {
      pending.push(chapter);
    }
  });
  renderChapterStatusColumn(progressDoneList, done);
  renderChapterStatusColumn(progressReviseList, revise);
  renderChapterStatusColumn(progressPendingList, pending);
}

function formatSignedPercent(value) {
  const number = Number(value || 0);
  const sign = number > 0 ? "+" : "";
  return `${sign}${number}%`;
}

function drawProgressChart(canvas, weeklyHistory) {
  if (!canvas) {
    return;
  }

  const ctx = canvas.getContext("2d");
  if (!ctx) {
    return;
  }

  const ratio = Math.min(window.devicePixelRatio || 1, 2);
  const width = Math.max(canvas.clientWidth || 0, 320);
  const height = Math.max(canvas.clientHeight || 0, 260);
  if (canvas.width !== Math.round(width * ratio) || canvas.height !== Math.round(height * ratio)) {
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
  }

  ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
  ctx.clearRect(0, 0, width, height);

  const pad = { top: 24, right: 18, bottom: 54, left: 44 };
  const chartW = width - pad.left - pad.right;
  const chartH = height - pad.top - pad.bottom;
  ctx.fillStyle = "rgba(255,255,255,0.08)";
  ctx.fillRect(0, 0, width, height);

  if (!weeklyHistory || !weeklyHistory.length) {
    ctx.fillStyle = "rgba(9, 18, 35, 0.7)";
    ctx.font = "600 16px Segoe UI, sans-serif";
    ctx.fillText("Save a few progress updates to see weekly comparisons here.", 24, 48);
    return;
  }

  const maxRate = 100;
  const weekGap = 18;
  const barCount = weeklyHistory.length;
  const barWidth = Math.max(38, Math.min(72, (chartW - weekGap * (barCount - 1)) / barCount));
  const baseY = pad.top + chartH;
  const gridSteps = [0, 25, 50, 75, 100];

  ctx.strokeStyle = "rgba(55, 78, 112, 0.28)";
  ctx.fillStyle = "rgba(41, 57, 86, 0.7)";
  ctx.font = "600 12px Segoe UI, sans-serif";
  gridSteps.forEach((step) => {
    const y = pad.top + chartH - (step / maxRate) * chartH;
    ctx.beginPath();
    ctx.moveTo(pad.left, y);
    ctx.lineTo(width - pad.right, y);
    ctx.stroke();
    ctx.fillText(`${step}%`, 10, y + 4);
  });

  weeklyHistory.forEach((week, index) => {
    const x = pad.left + index * (barWidth + weekGap);
    const total = Math.max(Number(week.total || 0), 1);
    const doneRate = Math.max(0, Math.min(100, (Number(week.done || 0) / total) * 100));
    const reviseRate = Math.max(0, Math.min(100, (Number(week.revise || 0) / total) * 100));
    const pendingRate = Math.max(0, Math.min(100, (Number(week.pending || 0) / total) * 100));
    const stack = [
      { key: "pending", value: pendingRate, color: "#ef4444" },
      { key: "revise", value: reviseRate, color: "#b7791f" },
      { key: "done", value: doneRate, color: "#16a34a" },
    ];

    let cursorY = baseY;
    stack.forEach((segment) => {
      const segmentHeight = chartH * (segment.value / 100);
      if (segmentHeight <= 0) {
        return;
      }
      cursorY -= segmentHeight;
      ctx.fillStyle = segment.color;
      ctx.fillRect(x, cursorY, barWidth, segmentHeight - 2);
    });

    ctx.fillStyle = "rgba(241, 245, 249, 0.94)";
    ctx.fillRect(x, pad.top + chartH - chartH * (Number(week.completion_rate || 0) / 100) - 2, barWidth, 2);

    ctx.fillStyle = "rgba(9, 18, 35, 0.8)";
    ctx.font = "700 12px Segoe UI, sans-serif";
    ctx.fillText(`${Number(week.completion_rate || 0).toFixed(0)}%`, x + 4, cursorY - 8);

    ctx.fillStyle = "rgba(10, 20, 34, 0.76)";
    ctx.font = "600 11px Segoe UI, sans-serif";
    const label = String(week.label || `W${index + 1}`).slice(0, 9);
    ctx.fillText(label, x, height - 22);
  });
}

function renderProgressSnapshot(snapshot) {
  latestProgressSnapshot = snapshot || null;
  const counts = (snapshot && snapshot.counts) || {};
  const topicMomentum = (snapshot && snapshot.topic_momentum) || {};
  const examTotals = (snapshot && snapshot.exam_totals) || {};
  const weeklyHistory = (snapshot && snapshot.weekly_history) || [];
  const weekOverWeek = (snapshot && snapshot.week_over_week) || {};
  if (progressDoneCount) {
    progressDoneCount.textContent = counts.done || 0;
  }
  if (progressReviseCount) {
    progressReviseCount.textContent = counts.revise || 0;
  }
  if (progressPendingCount) {
    progressPendingCount.textContent = counts.pending || 0;
  }
  if (progressTotalCount) {
    progressTotalCount.textContent = counts.total || 0;
  }
  if (progressReminderText) {
    const reminders = (snapshot && snapshot.reminders) || [];
    const extras = [];
    if (topicMomentum.mastery_signal) {
      extras.push(`Mastery: ${String(topicMomentum.mastery_signal).replace(/_/g, " ")}`);
    }
    if (topicMomentum.next_focus) {
      extras.push(topicMomentum.next_focus);
    }
    const examNames = Object.keys(examTotals || {});
    if (examNames.length) {
      const examSummary = examNames
        .slice(0, 2)
        .map((examName) => `${examName}: ${examTotals[examName].total || 0}`)
        .join(" | ");
      extras.push(`Exam spread: ${examSummary}`);
    }
    progressReminderText.textContent = reminders.length
      ? `${reminders.join(" ")}${extras.length ? ` ${extras.join(" ")}` : ""}`
      : `Track what is done, what still needs revision, and what is still pending so nothing silently slips through.${extras.length ? ` ${extras.join(" ")}` : ""}`;
  }

  if (progressWeekSummary) {
    progressWeekSummary.textContent = weekOverWeek.summary || "Weekly comparison will appear here.";
  }
  if (progressCurrentWeekRate) {
    progressCurrentWeekRate.textContent = `${Number((weekOverWeek.current && weekOverWeek.current.completion_rate) || counts.completion_rate || 0).toFixed(1)}%`;
  }
  if (progressPreviousWeekRate) {
    progressPreviousWeekRate.textContent = `${Number((weekOverWeek.previous && weekOverWeek.previous.completion_rate) || 0).toFixed(1)}%`;
  }
  if (progressImprovementRate) {
    progressImprovementRate.textContent = formatSignedPercent((weekOverWeek.delta && weekOverWeek.delta.completion_rate) || 0);
  }
  if (progressNeedFocus) {
    const focusText = topicMomentum.next_focus || "Keep reviewing weak topics.";
    const pendingCount = counts.pending || 0;
    progressNeedFocus.textContent = pendingCount ? `${pendingCount} pending` : focusText;
  }
  if (progressComparisonText) {
    const delta = weekOverWeek.delta || {};
    const focus = topicMomentum.next_focus || "Keep a steady revision loop.";
    progressComparisonText.textContent = weekOverWeek.summary
      ? `${weekOverWeek.summary} This week: ${counts.done || 0} done, ${counts.revise || 0} revise, ${counts.pending || 0} pending. Delta: done ${formatSignedPercent(delta.done || 0)}, revise ${formatSignedPercent(delta.revise || 0)}, pending ${formatSignedPercent(delta.pending || 0)}. ${focus}`
      : `This week: ${counts.done || 0} done, ${counts.revise || 0} revise, ${counts.pending || 0} pending. ${focus}`;
  }
  drawProgressChart(progressWeeklyCanvas, weeklyHistory);
  updateOverviewCommandCenter();
}

function renderChapterMasteryBoard(payload) {
  chapterMasterySnapshot = payload || null;
  renderProgressStatusFromChapterMastery(payload || null);
  if (!chapterMasteryCard || !chapterMasteryGrid) {
    return;
  }
  const chapters = (payload && payload.chapters) || [];
  chapterMasteryCard.classList.toggle("hidden", !chapters.length);
  if (chapterMasterySummary) {
    chapterMasterySummary.textContent = chapters.length
      ? `${chapters.length} chapters tracked across Physics, Chemistry, and Mathematics.`
      : "Your chapters will be color-coded by mastery level here.";
  }
  chapterMasteryGrid.innerHTML = "";
  if (!chapters.length) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = "No chapter mastery data yet.";
    chapterMasteryGrid.appendChild(empty);
    return;
  }
  chapters.forEach((chapter) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `chapter-chip chapter-${String(chapter.color || "grey").toLowerCase()}`;
    const scoreText = chapter.chapter_test_score !== null && chapter.chapter_test_score !== undefined ? `${Math.round(Number(chapter.chapter_test_score) || 0)}%` : "Not started";
    button.innerHTML = `
      <strong>${escapeHtml(chapter.chapter_name || "Chapter")}</strong>
      <span>${escapeHtml(String(chapter.subject || "").toUpperCase() || "GENERAL")} - ${escapeHtml(chapter.mastery_level || "not_started")} - ${escapeHtml(scoreText)}</span>
    `;
    button.addEventListener("click", () => {
      renderChapterDetailPanel(chapter);
    });
    chapterMasteryGrid.appendChild(button);
  });
  updateContextPanel(document.querySelector(".tab-panel.active")?.id || "");
}

function renderChapterDetailPanel(chapter) {
  if (!chapterDetailCard || !chapterDetailList) {
    return;
  }
  selectedChapterSnapshot = chapter || null;
  chapterDetailCard.classList.remove("hidden");
  chapterDetailCard.classList.add("chapter-summary-modal");
  chapterDetailList.innerHTML = "";
  if (chapterDetailSummary) {
    const score = chapter.chapter_test_score !== null && chapter.chapter_test_score !== undefined ? `${Math.round(Number(chapter.chapter_test_score) || 0)}%` : "Not started";
    chapterDetailSummary.textContent = `${chapter.chapter_name || "Chapter"} - Mastery: ${chapter.mastery_level || "not_started"} - Score: ${score}`;
  }
  const rows = [
    `Subject: ${chapter.subject || "-"}`,
    `Time spent: ${chapter.time_spent_total_minutes || 0} min`,
    `Revision count: ${chapter.revision_count || 0}`,
    `Weak subtopics: ${(chapter.weak_subtopics || []).join(", ") || "None"}`,
    `Strong subtopics: ${(chapter.strong_subtopics || []).join(", ") || "None"}`,
    `Revision scheduled: ${(chapter.revision_scheduled || []).join(", ") || "None"}`,
  ];
  rows.forEach((line) => {
    const row = document.createElement("div");
    row.className = "weekly-strategy-item";
    const text = document.createElement("p");
    text.className = "muted";
    text.textContent = line;
    row.appendChild(text);
    chapterDetailList.appendChild(row);
  });
}

function renderChapterAnalytics(payload) {
  chapterAnalyticsSnapshot = payload || null;
  if (!chapterAnalyticsCard || !chapterAnalyticsList) {
    return;
  }
  const averageScore = Number(payload && payload.average_score || 0).toFixed(1);
  const subjectAverages = payload && payload.subject_averages ? payload.subject_averages : {};
  chapterAnalyticsCard.classList.toggle("hidden", !Object.keys(subjectAverages).length && !averageScore);
  if (chapterAnalyticsSummary) {
    chapterAnalyticsSummary.textContent = `Average chapter score: ${averageScore}%`;
  }
  chapterAnalyticsList.innerHTML = "";
  const best = document.createElement("p");
  best.className = "muted";
  best.textContent = `Best chapter: ${payload && payload.best_chapter ? payload.best_chapter : "-"}`;
  chapterAnalyticsList.appendChild(best);
  Object.entries(subjectAverages || {}).forEach(([subject, score]) => {
    const row = document.createElement("div");
    row.className = "weekly-strategy-item";
    const title = document.createElement("strong");
    title.textContent = subject;
    const meta = document.createElement("p");
    meta.className = "muted";
    meta.textContent = `Average score: ${Number(score || 0).toFixed(1)}%`;
    row.append(title, meta);
    chapterAnalyticsList.appendChild(row);
  });
  updateContextPanel(document.querySelector(".tab-panel.active")?.id || "");
}

function renderChapterRevisionTracker(payload) {
  chapterRevisionSnapshot = payload || null;
  if (!chapterRevisionCard || !chapterRevisionList) {
    return;
  }
  const dueToday = [];
  const upcoming = [];
  (payload && payload.chapters ? payload.chapters : []).forEach((chapter) => {
    const level = String(chapter.mastery_level || "not_started").toLowerCase();
    if (level === "needs_revision" || level === "developing") {
      dueToday.push(chapter);
    } else if (level === "proficient") {
      upcoming.push(chapter);
    }
  });
  chapterRevisionCard.classList.toggle("hidden", !dueToday.length && !upcoming.length);
  if (chapterRevisionSummary) {
    chapterRevisionSummary.textContent = dueToday.length
      ? `${dueToday.length} chapter(s) need revision attention now.`
      : "Revision schedule is clear right now.";
  }
  chapterRevisionList.innerHTML = "";
  const combined = [...dueToday, ...upcoming].slice(0, 8);
  if (!combined.length) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = "Revision schedule will appear here.";
    chapterRevisionList.appendChild(empty);
    return;
  }
  combined.forEach((chapter) => {
    const row = document.createElement("div");
    row.className = "weekly-strategy-item";
    const title = document.createElement("strong");
    title.textContent = chapter.chapter_name || "Chapter";
    const meta = document.createElement("p");
    meta.className = "muted";
    meta.textContent = `${chapter.mastery_level || "not_started"} - ${chapter.chapter_test_score !== null && chapter.chapter_test_score !== undefined ? `${Math.round(Number(chapter.chapter_test_score) || 0)}%` : "No test yet"}`;
    row.append(title, meta);
    chapterRevisionList.appendChild(row);
  });
  updateContextPanel(document.querySelector(".tab-panel.active")?.id || "");
}

function hideChapterResumeUI() {
  chapterResumeBannerDismissedFor = "";
  if (chapterResumeBanner) {
    chapterResumeBanner.classList.add("hidden");
    chapterResumeBanner.innerHTML = "";
  }
  if (chapterResumeCard) {
    chapterResumeCard.classList.add("hidden");
    chapterResumeCard.innerHTML = "";
  }
}

function renderChapterResumeCard(summary) {
  if (!chapterResumeCard || !summary || !summary.resuming) {
    hideChapterResumeUI();
    return;
  }
  activeChapterResumeSummary = summary;
  const completed = Array.isArray(summary.subtopics_completed) ? summary.subtopics_completed : [];
  const remaining = Array.isArray(summary.subtopics_remaining) ? summary.subtopics_remaining : [];
  const current = summary.current_subtopic || {};
  const total = Number(current.total_subtopics || completed.length + remaining.length || 1);
  const done = Number(completed.length || 0);
  const percent = Math.max(0, Math.min(100, Number(summary.chapter_progress_percent || (done / Math.max(total, 1)) * 100)));
  const completedHtml = completed.length
    ? completed.map((item) => `<li><strong>${escapeHtml(item.name || "")}</strong> <span class="muted">(${escapeHtml(String(item.score ?? 0))}%)</span><br><span class="muted">${escapeHtml(item.completed_at || "")}</span></li>`).join("")
    : "<li class=\"muted\">No subtopics completed yet.</li>";
  const remainingHtml = remaining.length
    ? remaining.map((item) => `<li>${escapeHtml(item)}</li>`).join("")
    : "<li class=\"muted\">No remaining subtopics.</li>";
  const currentName = current.name || "Current subtopic";
  const currentNumber = current.subtopic_number || done + 1;
  const totalSubtopics = current.total_subtopics || total || 1;
  chapterResumeCard.classList.remove("hidden");
  chapterResumeCard.innerHTML = `
    <div class="chapter-completion-shell">
      <div class="card-header">
        <div>
          <p class="card-title">Resume ${escapeHtml(summary.unit_name || "Chapter")}</p>
          <p class="muted">${escapeHtml(String(summary.subject || "").toUpperCase() || "GENERAL")} - ${done} of ${totalSubtopics} subtopics complete</p>
        </div>
        <span class="pill">Resume</span>
      </div>
      <div class="chapter-progress-bar">
        <div class="chapter-progress-fill" style="width:${percent}%;"></div>
      </div>
      <div class="chapter-resume-grid">
        <div class="weekly-strategy-item">
          <strong>Completed subtopics</strong>
          <ul class="chapter-resume-list">${completedHtml}</ul>
        </div>
        <div class="weekly-strategy-item">
          <strong>Current subtopic</strong>
          <p class="memory-heading">${escapeHtml(currentName)}</p>
          <p class="muted">Subtopic ${currentNumber} of ${totalSubtopics}</p>
        </div>
        <div class="weekly-strategy-item">
          <strong>Remaining subtopics</strong>
          <ul class="chapter-resume-list">${remainingHtml}</ul>
        </div>
        <div class="weekly-strategy-item">
          <strong>Time spent so far</strong>
          <p class="memory-heading">${Number(summary.time_spent_so_far_minutes || 0).toFixed(1)} minutes</p>
          <p class="muted">Chapter test taken: ${summary.chapter_test_taken ? "Yes" : "No"}</p>
        </div>
      </div>
      <p class="chapter-resume-message">${escapeHtml(summary.resume_message || "")}</p>
      <div class="chapter-completion-actions">
        <button type="button" id="chapterResumeContinueBtn">Continue from where I left off</button>
      </div>
    </div>
  `;
  const showBanner = chapterResumeBannerDismissedFor !== (activeProfile ? activeProfile.name : "");
  if (showBanner) {
    chapterResumeBanner.classList.remove("hidden");
    chapterResumeBanner.innerHTML = `
      <div class="chapter-resume-banner-inner">
        <span>You have an active session: ${escapeHtml(summary.unit_name || "Chapter")} - ${done} of ${totalSubtopics} subtopics complete. Continue?</span>
        <div class="chapter-resume-banner-actions">
          <button type="button" id="chapterResumeGoBtn" class="ghost-button">Go to session</button>
          <button type="button" id="chapterResumeCloseBtn" class="ghost-button chapter-resume-close-btn" aria-label="Close resume notice">Close</button>
        </div>
      </div>
    `;
  } else {
    hideChapterResumeBanner();
  }
  const continueBtn = chapterResumeCard.querySelector("#chapterResumeContinueBtn");
  const goBtn = chapterResumeBanner ? chapterResumeBanner.querySelector("#chapterResumeGoBtn") : null;
  const closeBtn = chapterResumeBanner ? chapterResumeBanner.querySelector("#chapterResumeCloseBtn") : null;
  const continueSession = () => {
    chapterResumeDismissedFor = activeProfile ? activeProfile.name : chapterResumeDismissedFor;
    hideChapterResumeUI();
    setActiveTab("tutorTab");
    if (summary.resume_message) {
      appendMessage("tutor", "tutor", summary.resume_message);
    }
  };
  if (continueBtn) {
    continueBtn.addEventListener("click", async () => {
      await refreshActiveChapterSession();
      continueSession();
    });
  }
  if (goBtn) {
    goBtn.addEventListener("click", async () => {
      await refreshActiveChapterSession();
      setActiveTab("tutorTab");
      chapterResumeCard.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }
  if (closeBtn) {
    closeBtn.addEventListener("click", () => {
      chapterResumeBannerDismissedFor = activeProfile ? activeProfile.name : chapterResumeBannerDismissedFor;
      hideChapterResumeBanner();
    });
  }
}

function hideChapterResumeBanner() {
  if (chapterResumeBanner) {
    chapterResumeBanner.classList.add("hidden");
    chapterResumeBanner.innerHTML = "";
  }
}

async function loadChapterResumeState(force = false) {
  if (!activeProfile) {
    hideChapterResumeUI();
    return null;
  }
  const studentId = activeProfile.name;
  if (!force && chapterResumeDismissedFor === studentId) {
    hideChapterResumeUI();
    return activeChapterResumeSummary;
  }
  if (!force && chapterResumeLoadedFor === studentId && activeChapterResumeSummary) {
    if (activeChapterResumeSummary.resuming) {
      renderChapterResumeCard(activeChapterResumeSummary);
    }
    return activeChapterResumeSummary;
  }
  try {
    const response = await fetch(`/api/session/resume-summary/${encodeURIComponent(studentId)}`);
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Could not load the resume summary.");
    }
    chapterResumeLoadedFor = studentId;
    activeChapterResumeSummary = payload || null;
    if (payload && payload.resuming) {
      renderChapterResumeCard(payload);
      return payload;
    }
    hideChapterResumeUI();
    return payload;
  } catch (error) {
    console.warn("Could not load chapter resume summary:", error);
    hideChapterResumeUI();
    return null;
  }
}

async function resetChapterFromUI(chapter) {
  if (!activeProfile || !chapter) {
    return;
  }
  const chapterName = chapter.unit_name || chapter.chapter_name || chapter.topic || "this chapter";
  const confirmReset = window.confirm(`Are you sure you want to restart ${chapterName}? Your previous scores will be saved in history but your current progress will be cleared.`);
  if (!confirmReset) {
    return;
  }
  try {
    const response = await fetch("/api/session/reset-chapter", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        student_id: activeProfile.name,
        unit_name: chapter.unit_name || chapterName,
        subject: chapter.subject || "",
      }),
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Could not reset that chapter.");
    }
    activeChapterSession = null;
    activeChapterSubtopic = null;
    selectedChapterSnapshot = null;
    activeChapterResumeSummary = null;
    chapterResumeLoadedFor = "";
    chapterResumeDismissedFor = "";
    hideChapterResumeUI();
    closeChapterDetailPanel();
    if (chapterCompletionCard) {
      chapterCompletionCard.classList.add("hidden");
      chapterCompletionCard.innerHTML = "";
    }
    clearChapterTestContainer();
    appendMessage("tutor", "tutor", `Chapter reset. You can start ${chapterName} fresh whenever you are ready.`);
    await refreshWeeklyPlan();
    await refreshJourneyDashboard();
    await fetchProgress(activeProfile.name);
    await loadChapterResumeState(true);
  } catch (error) {
    appendMessage("tutor", "tutor", `Could not reset that chapter right now: ${error.message}`);
  }
}

function clearChapterTimers() {
  if (activeChapterTestInterval) {
    window.clearInterval(activeChapterTestInterval);
    activeChapterTestInterval = null;
  }
  if (activeChapterBreakInterval) {
    window.clearInterval(activeChapterBreakInterval);
    activeChapterBreakInterval = null;
  }
  activeChapterBreakEndAt = null;
}

function formatChapterClock(totalSeconds) {
  const safeSeconds = Math.max(0, Math.floor(Number(totalSeconds) || 0));
  const minutes = String(Math.floor(safeSeconds / 60)).padStart(2, "0");
  const seconds = String(safeSeconds % 60).padStart(2, "0");
  return `${minutes}:${seconds}`;
}

function getActiveChapterTitle() {
  return String(
    (selectedChapterSnapshot && selectedChapterSnapshot.chapter_name) ||
    (activeChapterSession && activeChapterSession.unit_name) ||
    (activeChapterSubtopic && activeChapterSubtopic.chapter_name) ||
    "this chapter"
  ).trim();
}

function getActiveChapterSubject() {
  return String(
    (selectedChapterSnapshot && selectedChapterSnapshot.subject) ||
    (activeChapterSession && activeChapterSession.subject) ||
    (activeChapterSubtopic && activeChapterSubtopic.subject) ||
    ""
  ).trim();
}

function closeChapterDetailPanel() {
  if (!chapterDetailCard) {
    return;
  }
  chapterDetailCard.classList.add("hidden");
  chapterDetailCard.classList.remove("chapter-summary-modal");
}

function renderChapterCompletionCard({ unitName, questionCount = 15, durationMinutes = 30, breakMode = false } = {}) {
  if (!chapterCompletionCard) {
    return;
  }
  activeChapterCompletionMode = {
    unitName: unitName || getActiveChapterTitle(),
    questionCount,
    durationMinutes,
    breakMode,
  };
  chapterCompletionCard.classList.remove("hidden");
  chapterCompletionCard.innerHTML = `
    <div class="chapter-completion-shell">
      <div class="card-header">
        <div>
          <p class="card-title">Chapter Test Ready</p>
          <p class="muted">You have completed all subtopics in ${escapeHtml(activeChapterCompletionMode.unitName)}. Time for your Chapter Test - ${questionCount} questions, ${durationMinutes} minutes, JEE Main format.</p>
        </div>
        <span class="pill">Ready</span>
      </div>
      <div class="chapter-completion-actions">
        <button type="button" id="chapterTestNowBtn">Take Chapter Test Now</button>
        <button type="button" id="chapterTestBreakBtn" class="ghost-button">Take a 5 minute break first</button>
      </div>
      <p class="muted chapter-completion-timer" id="chapterCompletionTimer">Break not started.</p>
    </div>
  `;
  const nowBtn = chapterCompletionCard.querySelector("#chapterTestNowBtn");
  const breakBtn = chapterCompletionCard.querySelector("#chapterTestBreakBtn");
  const timerLine = chapterCompletionCard.querySelector("#chapterCompletionTimer");
  if (nowBtn) {
    nowBtn.addEventListener("click", async () => {
      await loadChapterTestForCurrentSession({ immediate: true });
    });
  }
  if (breakBtn) {
    breakBtn.addEventListener("click", () => {
      startChapterBreakCountdown(timerLine, breakBtn);
    });
  }
}

function startChapterBreakCountdown(timerLine, breakBtn) {
  clearChapterTimers();
  activeChapterBreakEndAt = Date.now() + 5 * 60 * 1000;
  const tick = () => {
    const remaining = Math.max(0, Math.ceil((activeChapterBreakEndAt - Date.now()) / 1000));
    if (timerLine) {
      timerLine.textContent = remaining > 0
        ? `Break time remaining: ${formatChapterClock(remaining)}`
        : "Break complete. Loading your chapter test...";
    }
    if (breakBtn) {
      breakBtn.disabled = remaining > 0;
      breakBtn.textContent = remaining > 0 ? `Take a 5 minute break first (${formatChapterClock(remaining)})` : "Loading...";
    }
    if (remaining <= 0) {
      clearChapterTimers();
      window.setTimeout(() => {
        loadChapterTestForCurrentSession({ immediate: false });
      }, 200);
    }
  };
  tick();
  activeChapterBreakInterval = window.setInterval(tick, 1000);
}

function updateChapterTestTimer() {
  if (!chapterTestContainer) {
    return;
  }
  const timer = chapterTestContainer.querySelector("[data-chapter-test-timer]");
  if (!timer) {
    return;
  }
  if (!activeChapterTestStartedAt) {
    timer.textContent = "30:00";
    return;
  }
  const totalSeconds = Math.max(0, 30 * 60 - Math.floor((Date.now() - activeChapterTestStartedAt) / 1000));
  timer.textContent = formatChapterClock(totalSeconds);
  if (totalSeconds <= 0) {
    const submitBtn = chapterTestContainer.querySelector("#chapterTestSubmitBtn");
    if (submitBtn && !submitBtn.disabled) {
      submitBtn.click();
    }
  }
}

function clearChapterTestContainer() {
  if (!chapterTestContainer) {
    return;
  }
  chapterTestContainer.classList.add("hidden");
  chapterTestContainer.innerHTML = "";
  activeChapterTest = null;
  activeChapterTestStartedAt = null;
  activeChapterTestAnswers = [];
  clearChapterTimers();
}

function renderChapterTestReport(report, summary) {
  if (!chapterTestContainer) {
    return;
  }
  const chapterSummary = (report && report.chapter_summary) || {};
  const weakSubtopics = Array.isArray(report && report.weak_subtopics) ? report.weak_subtopics : [];
  const strongSubtopics = Array.isArray(report && report.strong_subtopics) ? report.strong_subtopics : [];
  const revisionScheduled = Array.isArray(report && report.revision_scheduled) ? report.revision_scheduled : [];
  const nextSteps = Array.isArray(summary && summary.next_steps) ? summary.next_steps : revisionScheduled;
  const subtopicScores = chapterSummary.subtopic_scores || {};
  const masteryLevel = String((report && report.mastery_level) || "needs_revision").trim();
  const score = Number((report && report.score) || (summary && summary.score) || 0);
  const scoreLabel = `${Math.round(score)}%`;
  chapterTestContainer.classList.remove("hidden");
  chapterTestContainer.innerHTML = `
    <div class="chapter-test-shell">
      <div class="card-header">
        <div>
          <p class="card-title">Chapter Test Result</p>
          <p class="muted">Score ${scoreLabel} - ${escapeHtml(masteryLevel.replace(/_/g, " "))}</p>
        </div>
        <span class="pill">${escapeHtml(masteryLevel)}</span>
      </div>
      <div class="chapter-test-list">
        <div class="weekly-strategy-item">
          <strong>Subtopic breakdown</strong>
          ${Object.keys(subtopicScores).length ? Object.entries(subtopicScores).map(([name, value]) => `<p class="muted">${escapeHtml(name)}: ${Number(value || 0).toFixed(1)}%</p>`).join("") : '<p class="muted">No subtopic breakdown was returned.</p>'}
        </div>
        <div class="weekly-strategy-item">
          <strong>Weak areas</strong>
          ${weakSubtopics.length ? weakSubtopics.map((item) => `<p class="muted">${escapeHtml(item)}</p>`).join("") : '<p class="muted">None flagged.</p>'}
        </div>
        <div class="weekly-strategy-item">
          <strong>Strong areas</strong>
          ${strongSubtopics.length ? strongSubtopics.map((item) => `<p class="muted">${escapeHtml(item)}</p>`).join("") : '<p class="muted">No strong areas recorded yet.</p>'}
        </div>
        <div class="weekly-strategy-item">
          <strong>Revision schedule</strong>
          ${revisionScheduled.length ? revisionScheduled.map((item) => `<p class="muted">${escapeHtml(item)}</p>`).join("") : '<p class="muted">No revision scheduled right now.</p>'}
        </div>
        <div class="weekly-strategy-item">
          <strong>Next steps</strong>
          ${nextSteps.length ? nextSteps.map((item) => `<p class="muted">${escapeHtml(item)}</p>`).join("") : '<p class="muted">Move on to the next chapter or request more practice.</p>'}
        </div>
      </div>
      <div class="chapter-test-actions">
        <button type="button" class="ghost-button" id="chapterTestBackToBoardBtn">Back to chapter board</button>
        <button type="button" id="chapterTestStartNextPracticeBtn">Want more practice?</button>
      </div>
    </div>
  `;
  const backBtn = chapterTestContainer.querySelector("#chapterTestBackToBoardBtn");
  const nextPracticeBtn = chapterTestContainer.querySelector("#chapterTestStartNextPracticeBtn");
  if (backBtn) {
    backBtn.addEventListener("click", () => {
      openPlanSubtab("progress");
      refreshProgress(activeProfile ? activeProfile.name : "");
    });
  }
  if (nextPracticeBtn) {
    nextPracticeBtn.addEventListener("click", async () => {
      if (!activeProfile) {
        return;
      }
      try {
        const response = await fetch("/api/session/extend-practice", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            student_id: activeProfile.name,
            unit_name: getActiveChapterTitle(),
            practice_type: "5_questions",
          }),
        });
        const payload = await response.json();
        if (!response.ok) {
          throw new Error(payload.detail || "Could not load more practice.");
        }
        appendMessage("tutor", "tutor", `Here are five more JEE questions for ${getActiveChapterTitle()}.`);
        renderTutorPracticeSet(payload.questions || [], null, { chapterMode: true });
      } catch (error) {
        appendMessage("tutor", "tutor", `Could not load more practice right now: ${error.message}`);
      }
    });
  }
  chapterTestContainer.scrollIntoView({ behavior: "smooth", block: "start" });
}

function renderChapterTest(questions, meta = {}) {
  if (!chapterTestContainer) {
    return;
  }
  clearChapterTimers();
  activeChapterTest = {
    questions: Array.isArray(questions) ? questions.slice(0, 15) : [],
    unit_name: meta.unit_name || getActiveChapterTitle(),
    subject: meta.subject || getActiveChapterSubject(),
    duration_minutes: Number(meta.duration_minutes || 30),
    marking: meta.marking || "+4 correct, -1 wrong",
  };
  activeChapterTestAnswers = new Array(activeChapterTest.questions.length).fill("");
  activeChapterTestStartedAt = Date.now();
  chapterTestContainer.classList.remove("hidden");
  chapterTestContainer.innerHTML = `
    <div class="chapter-test-shell">
      <div class="card-header">
        <div>
          <p class="card-title">Chapter Test - ${escapeHtml(activeChapterTest.unit_name)}</p>
          <p class="muted">All questions are shown at once. JEE Main format - ${activeChapterTest.questions.length} questions - ${activeChapterTest.duration_minutes} minutes - ${escapeHtml(activeChapterTest.marking)}</p>
        </div>
        <span class="pill chapter-test-timer" data-chapter-test-timer>30:00</span>
      </div>
      <div class="chapter-test-list" id="chapterTestQuestionList"></div>
      <div class="chapter-test-actions">
        <button type="button" id="chapterTestSubmitBtn">Submit Test</button>
        <button type="button" class="ghost-button" id="chapterTestCancelBtn">Hide test</button>
      </div>
      <div class="chapter-test-report hidden" id="chapterTestReport"></div>
    </div>
  `;
  const questionList = chapterTestContainer.querySelector("#chapterTestQuestionList");
  const submitBtn = chapterTestContainer.querySelector("#chapterTestSubmitBtn");
  const cancelBtn = chapterTestContainer.querySelector("#chapterTestCancelBtn");
  const reportPanel = chapterTestContainer.querySelector("#chapterTestReport");
  activeChapterTest.questions.forEach((question, index) => {
    const card = document.createElement("div");
    card.className = "chapter-test-question-card";
    card.dataset.questionIndex = String(index);

    const header = document.createElement("div");
    const title = document.createElement("p");
    title.className = "card-title";
    title.textContent = `Question ${index + 1}`;
    const metaLine = document.createElement("p");
    metaLine.className = "muted";
    metaLine.textContent = `${question.subtopic || activeChapterTest.unit_name} - ${question.difficulty || "medium"}`;
    header.append(title, metaLine);

    const questionBody = document.createElement("div");
    questionBody.className = "chapter-test-question";
    renderMarkdownElement(questionBody, question.question || "Question unavailable.");

    const options = document.createElement("div");
    options.className = "chapter-test-options";
    const questionName = `chapter-test-${index}`;
    (question.options || []).slice(0, 4).forEach((option, optionIndex) => {
      const letter = _checkpointOptionLabel(optionIndex);
      const optionLabel = document.createElement("label");
      optionLabel.className = "chapter-test-option";
      optionLabel.dataset.option = letter;
      const input = document.createElement("input");
      input.type = "radio";
      input.name = questionName;
      input.value = letter;
      input.checked = activeChapterTestAnswers[index] === letter;
      const optionText = document.createElement("span");
      optionText.textContent = `${letter}. ${option}`;
      input.addEventListener("change", () => {
        activeChapterTestAnswers[index] = letter;
        options.querySelectorAll(".chapter-test-option").forEach((label) => {
          label.classList.toggle("selected", label.dataset.option === letter);
        });
      });
      optionLabel.append(input, optionText);
      if (input.checked) {
        optionLabel.classList.add("selected");
      }
      options.appendChild(optionLabel);
    });

    card.append(header, questionBody, options);
    questionList.appendChild(card);
  });

  const updateTimer = () => {
    if (!activeChapterTestStartedAt || !chapterTestContainer) {
      return;
    }
    const remainingSeconds = Math.max(0, Math.round((activeChapterTest.duration_minutes * 60) - ((Date.now() - activeChapterTestStartedAt) / 1000)));
    const timer = chapterTestContainer.querySelector("[data-chapter-test-timer]");
    if (timer) {
      timer.textContent = formatChapterClock(remainingSeconds);
    }
    if (remainingSeconds <= 0) {
      if (submitBtn && !submitBtn.disabled) {
        submitBtn.click();
      }
    }
  };
  updateTimer();
  activeChapterTestInterval = window.setInterval(updateTimer, 1000);

  const submitChapterTest = async () => {
    if (!activeProfile || !activeChapterTest) {
      return;
    }
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = "Submitting...";
    }
    const questions = activeChapterTest.questions || [];
    const selectedAnswers = questions.map((question, index) => activeChapterTestAnswers[index] || "");
    let correctCount = 0;
    questions.forEach((question, index) => {
      const correct = String(question.correct || question.correct_answer || "").trim().toUpperCase();
      if (selectedAnswers[index] && selectedAnswers[index] === correct) {
        correctCount += 1;
      }
    });
    const wrongCount = Math.max(0, questions.length - correctCount);
    const rawMarks = (correctCount * 4) - wrongCount;
    const maxMarks = Math.max(1, questions.length * 4);
    const score = Math.max(0, Math.round((rawMarks / maxMarks) * 100));
    const body = {
      student_id: activeProfile.name,
      unit_name: activeChapterTest.unit_name || getActiveChapterTitle(),
      subject: activeChapterTest.subject || getActiveChapterSubject(),
      score,
      answers: selectedAnswers,
      time_taken_minutes: Math.max(1, Math.round((Date.now() - activeChapterTestStartedAt) / 60000)),
    };
    console.log("CHAPTER TEST SUBMIT REQUEST:", body);
    try {
      const response = await fetch("/api/session/submit-chapter-test", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.detail || "Could not submit chapter test.");
      }
      const masteryReport = payload.mastery_report || payload;
      renderChapterTestReport(masteryReport, {
        score,
        correctCount,
        wrongCount,
        answers: selectedAnswers,
        next_steps: payload.next_steps || masteryReport.revision_scheduled || [],
      });
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = "Submitted";
      }
      await refreshEngagementAfterLPAward(payload.lp_awards);
      await refreshJourneyDashboard();
    } catch (error) {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = "Submit Test";
      }
      if (reportPanel) {
        reportPanel.classList.remove("hidden");
        reportPanel.innerHTML = `<p class="muted">Could not submit the chapter test: ${escapeHtml(error.message)}</p>`;
      }
    } finally {
      clearChapterTimers();
    }
  };

  if (submitBtn) {
    submitBtn.addEventListener("click", submitChapterTest);
  }
  if (cancelBtn) {
    cancelBtn.addEventListener("click", () => {
      clearChapterTimers();
      chapterTestContainer.classList.add("hidden");
      chapterTestContainer.innerHTML = "";
    });
  }
  chapterTestContainer.scrollIntoView({ behavior: "smooth", block: "start" });
}

async function loadChapterTestForCurrentSession({ immediate = true } = {}) {
  if (!activeProfile) {
    return;
  }
  const unitName = getActiveChapterTitle();
  if (!unitName) {
    return;
  }
  openPlanSubtab("progress");
  if (chapterTestContainer) {
    chapterTestContainer.classList.remove("hidden");
    chapterTestContainer.innerHTML = `<p class="muted">Loading chapter test for ${escapeHtml(unitName)}...</p>`;
  }
  try {
    const response = await fetch(`/api/session/generate-chapter-test/${encodeURIComponent(activeProfile.name)}/${encodeURIComponent(unitName)}`);
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Could not load the chapter test.");
    }
    if (chapterCompletionCard) {
      chapterCompletionCard.classList.add("hidden");
    }
    renderChapterTest(payload.questions || [], payload);
  } catch (error) {
    if (chapterTestContainer) {
      chapterTestContainer.classList.remove("hidden");
      chapterTestContainer.innerHTML = `<p class="muted">Could not load the chapter test: ${escapeHtml(error.message)}</p>`;
    }
  }
}

async function startSelectedChapterSession() {
  if (!activeProfile || !selectedChapterSnapshot) {
    return;
  }
  try {
    const response = await fetch("/api/session/start-chapter", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        student_id: activeProfile.name,
        unit_name: selectedChapterSnapshot.chapter_name || "",
        subject: selectedChapterSnapshot.subject || "",
      }),
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Could not start chapter session.");
    }
    activeChapterSession = payload.session || null;
    activeChapterSubtopic = payload.first_subtopic || null;
    activeChapterResumeSummary = null;
    chapterResumeLoadedFor = "";
    chapterResumeDismissedFor = "";
    selectedChapterSnapshot = {
      ...(selectedChapterSnapshot || {}),
      active_session: payload.session || {},
      first_subtopic: payload.first_subtopic || {},
    };
    if (chapterDetailSummary && payload.first_subtopic) {
      chapterDetailSummary.textContent = `${selectedChapterSnapshot.chapter_name || "Chapter"} - Starting ${payload.first_subtopic.subtopic_name || "the first subtopic"}`;
    }
    setActiveTab("tutorTab");
    appendMessage("tutor", "tutor", `We are starting ${selectedChapterSnapshot.chapter_name || "this chapter"} from ${payload.first_subtopic.subtopic_name || "the first subtopic"}. I will teach the full chapter one subtopic at a time and checkpoint after each part.`);
  } catch (error) {
    appendMessage("tutor", "tutor", `Could not start the chapter session: ${error.message}`);
  }
}

async function refreshActiveChapterSession() {
  if (!activeProfile) {
    return null;
  }
  try {
    const response = await fetch(`/api/session/current-subtopic/${encodeURIComponent(activeProfile.name)}`);
    const payload = await response.json();
    if (!response.ok) {
      return null;
    }
    const current = (payload && payload.current_subtopic) || null;
    activeChapterSubtopic = current && current.subtopic_id ? current : null;
    activeChapterSession = activeChapterSubtopic ? {
      student_id: activeProfile.name,
      unit_name: activeChapterSubtopic.chapter_name || activeChapterSubtopic.unit_name || "",
      subject: activeChapterSubtopic.subject || "",
      status: "in_progress",
    } : null;
    return activeChapterSubtopic;
  } catch (error) {
    console.warn("Could not refresh chapter session:", error);
    return null;
  }
}

function isChapterCheckpointActive() {
  return Boolean(activeChapterSubtopic && activeChapterSubtopic.subtopic_id);
}

async function completeChapterSubtopicFromCheckpoint(checkpointScore, timeSpentMinutes = 0) {
  if (!activeProfile || !isChapterCheckpointActive()) {
    return null;
  }
  try {
    const body = {
      student_id: activeProfile.name,
      subtopic_id: activeChapterSubtopic.subtopic_id || "",
      checkpoint_score: checkpointScore,
      time_spent_minutes: timeSpentMinutes || Math.max(1, Math.round(((activeChapterSubtopic.estimated_minutes || 0) || 1))),
    };
    console.log("CHAPTER SUBTOPIC COMPLETE REQUEST:", body);
    const response = await fetch("/api/session/complete-subtopic", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Could not complete the subtopic checkpoint.");
    }
    await refreshEngagementAfterLPAward(payload.lp_awards);
    activeChapterSession = payload.session || activeChapterSession;
    activeChapterSubtopic = payload.next_subtopic || null;
    if (selectedChapterSnapshot) {
      selectedChapterSnapshot = {
        ...(selectedChapterSnapshot || {}),
        active_session: payload.session || activeChapterSession || {},
        first_subtopic: activeChapterSubtopic || selectedChapterSnapshot.first_subtopic || {},
      };
    }
    if (payload.ready_for_chapter_test) {
      appendMessage("tutor", "tutor", `${payload.encouragement || "That subtopic is complete."} The chapter test is ready whenever you are.`);
      openPlanSubtab("progress");
      renderChapterCompletionCard({
        unitName: selectedChapterSnapshot && selectedChapterSnapshot.chapter_name ? selectedChapterSnapshot.chapter_name : (activeChapterSession && activeChapterSession.unit_name) || getActiveChapterTitle(),
        questionCount: 15,
        durationMinutes: 30,
      });
    } else if (payload.next_subtopic) {
      appendMessage("tutor", "tutor", `${payload.encouragement || "Good work."} Next we move to ${payload.next_subtopic.subtopic_name || "the next subtopic"}.`);
    }
    await refreshJourneyDashboard();
    await fetchStorageStatus(activeProfile.name);
    return payload;
  } catch (error) {
    console.warn("Could not complete chapter subtopic:", error);
    appendMessage("tutor", "tutor", `I saved the checkpoint, but the chapter session needs another pass: ${error.message}`);
    return null;
  }
}

function renderSummaryPanel(summaryText) {
  if (!summaryPanel) {
    return;
  }
  summaryPanel.innerHTML = "";
  activeSummaryText = summaryText || "";
  if (!summaryText) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = "A quick crisp summary of the latest explanation will appear here.";
    summaryPanel.appendChild(empty);
    return;
  }

  const heading = document.createElement("h3");
  heading.textContent = "Quick Summary";
  summaryPanel.appendChild(heading);

  const lines = String(summaryText)
    .split(/\n+/)
    .map((line) => line.trim())
    .filter(Boolean);

  const list = document.createElement("div");
  list.className = "reasoning-list";
  lines.forEach((line) => {
    const item = document.createElement("div");
    item.className = "reasoning-card";
    item.textContent = line.replace(/^[-*]\s*/, "");
    list.appendChild(item);
  });
  summaryPanel.appendChild(list);
}

function renderLiveSources(sources) {
  if (!liveSourcesList) {
    return;
  }

  liveSourcesList.innerHTML = "";
  if (!sources || !sources.length) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = "No live sources yet.";
    liveSourcesList.appendChild(empty);
    return;
  }

  sources.forEach((source) => {
    const link = document.createElement("a");
    link.className = "source-chip";
    link.href = source.url || "#";
    link.target = "_blank";
    link.rel = "noreferrer noopener";
    link.textContent = source.label || source.kind || "Source";
    liveSourcesList.appendChild(link);
  });
}

function renderVisualLearning(visual) {
  if (!visualLearningPanel) {
    return;
  }

  visualLearningPanel.innerHTML = "";
  if (!visual) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = "Ask the tutor to explain a concept, and the visual scene will appear here.";
    visualLearningPanel.appendChild(empty);
    renderConceptCanvas({
      title: "Concept Bridge",
      scenario: "Ask a concept question and I will map it into cause, rule, and effect.",
      animation: { type: "concept_flow", duration_ms: 3600, axes: { x: "cause", y: "effect" } },
      scene_config: { interaction_hint: "Try a concept prompt like 'Teach this concept visually'." },
      frames: [
        "Frame 1: Start with the cause or starting point.",
        "Frame 2: Identify the rule that connects the idea.",
        "Frame 3: Watch the effect or result appear.",
        "Frame 4: Retell the full chain in your own words.",
      ],
      case_study: "This fallback keeps the 3D board useful even before a topic-specific scene loads.",
      mastery: { mastery_tier: "Concept Bridge", chapter_unlock: "General concept mapping", reward_points: 16 },
    });
    window.dispatchEvent(new CustomEvent("alt:concept-visual", { detail: null }));
    return;
  }

  if (visual.mastery) {
    const masteryRow = document.createElement("div");
    masteryRow.className = "weekly-strategy-chip-row";

    const masteryChip = document.createElement("span");
    masteryChip.className = "focus-pill strength-pill";
    masteryChip.textContent = visual.mastery.mastery_tier || "Concept Bridge";
    masteryRow.appendChild(masteryChip);

    const unlockChip = document.createElement("span");
    unlockChip.className = "focus-pill";
    unlockChip.textContent = visual.mastery.chapter_unlock || "Chapter unlock";
    masteryRow.appendChild(unlockChip);

    const rewardChip = document.createElement("span");
    rewardChip.className = "focus-pill warning-pill";
    rewardChip.textContent = `+${visual.mastery.reward_points || 0} points`;
    masteryRow.appendChild(rewardChip);

    visualLearningPanel.appendChild(masteryRow);
  }

  const title = document.createElement("h3");
  title.textContent = visual.title;

  const scenario = document.createElement("p");
  scenario.className = "caption-text";
  scenario.textContent = visual.scenario;

  const interactionHint = visual.scene_config && visual.scene_config.interaction_hint ? document.createElement("p") : null;
  if (interactionHint) {
    interactionHint.className = "muted visual-hint";
    interactionHint.textContent = visual.scene_config.interaction_hint;
  }

  const frames = document.createElement("div");
  frames.className = "visual-frames";
  (visual.frames || []).forEach((frame) => {
    const card = document.createElement("div");
    card.className = "visual-frame-card";
    card.textContent = frame;
    frames.appendChild(card);
  });

  const caseStudy = document.createElement("p");
  caseStudy.className = "muted";
  caseStudy.textContent = visual.case_study;

  visualLearningPanel.appendChild(title);
  visualLearningPanel.appendChild(scenario);
  if (interactionHint) {
    visualLearningPanel.appendChild(interactionHint);
  }
  visualLearningPanel.appendChild(frames);
  visualLearningPanel.appendChild(caseStudy);
  renderSummaryPanel("");
  setActiveStudioPane("threeConceptPanel");
  window.requestAnimationFrame(() => {
    renderConceptCanvas(visual);
    window.dispatchEvent(new CustomEvent("alt:concept-visual", { detail: visual || null }));
  });
}

function stopConceptAnimation() {
  if (activeConceptAnimation) {
    window.cancelAnimationFrame(activeConceptAnimation);
    activeConceptAnimation = null;
  }
}

function drawCanvasLabel(ctx, text, x, y, align = "left") {
  ctx.save();
  ctx.fillStyle = "rgba(247, 247, 247, 0.92)";
  ctx.font = "12px 'Segoe UI', sans-serif";
  ctx.textAlign = align;
  ctx.fillText(text, x, y);
  ctx.restore();
}

function renderConceptCanvas(visual) {
  if (!conceptCanvas) {
    return;
  }

  stopConceptAnimation();
  const ctx = conceptCanvas.getContext("2d");
  if (!ctx) {
    return;
  }

  const width = conceptCanvas.width;
  const height = conceptCanvas.height;

  const clearBoard = (title, subtitle) => {
    ctx.clearRect(0, 0, width, height);
    const gradient = ctx.createLinearGradient(0, 0, width, height);
    gradient.addColorStop(0, "#14213d");
    gradient.addColorStop(1, "#1f3b73");
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, width, height);
    drawCanvasLabel(ctx, title, 18, 24);
    drawCanvasLabel(ctx, subtitle, 18, 42);
  };

  if (!visual || !visual.animation) {
    clearBoard("Concept Motion Board", "Ask for a concept and this space will animate the idea.");
    const nodes = [
      { x: 110, y: 130, label: "Cause", color: "#60a5fa" },
      { x: 260, y: 88, label: "Rule", color: "#7dd3fc" },
      { x: 410, y: 150, label: "Effect", color: "#fbbf24" },
    ];
    ctx.strokeStyle = "rgba(219, 234, 254, 0.48)";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(nodes[0].x + 20, nodes[0].y);
    ctx.lineTo(nodes[1].x - 20, nodes[1].y);
    ctx.lineTo(nodes[2].x - 20, nodes[2].y);
    ctx.stroke();
    nodes.forEach((node, index) => {
      ctx.fillStyle = node.color;
      ctx.beginPath();
      ctx.arc(node.x, node.y, 22, 0, Math.PI * 2);
      ctx.fill();
      drawCanvasLabel(ctx, node.label, node.x, node.y + 42, "center");
    });
    return;
  }

  const animation = visual.animation;
  const duration = animation.duration_ms || 3600;
  const start = performance.now();

  const drawScene = (timestamp) => {
    const progress = ((timestamp - start) % duration) / duration;
    clearBoard(visual.title, visual.scenario || "Visual scene");

    if (animation.type === "projectile") {
      ctx.strokeStyle = "rgba(255,255,255,0.2)";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(52, 208);
      ctx.lineTo(470, 208);
      ctx.moveTo(82, 32);
      ctx.lineTo(82, 208);
      ctx.stroke();

      ctx.fillStyle = "#2f4858";
      ctx.fillRect(72, 88, 34, 120);
      ctx.fillStyle = "#ffd166";
      ctx.beginPath();
      ctx.arc(420, 198, 12, 0, Math.PI * 2);
      ctx.fill();

      const x = 96 + progress * 300;
      const y = 98 + 118 * Math.pow(progress - 0.12, 2);
      ctx.strokeStyle = "rgba(255, 209, 102, 0.35)";
      ctx.beginPath();
      for (let step = 0; step <= 1; step += 0.02) {
        const curveX = 96 + step * 300;
        const curveY = 98 + 118 * Math.pow(step - 0.12, 2);
        if (step === 0) {
          ctx.moveTo(curveX, curveY);
        } else {
          ctx.lineTo(curveX, curveY);
        }
      }
      ctx.stroke();

      ctx.fillStyle = "#ff7f50";
      ctx.beginPath();
      ctx.arc(x, y, 10, 0, Math.PI * 2);
      ctx.fill();

      drawCanvasLabel(ctx, "horizontal distance", 455, 226, "right");
      drawCanvasLabel(ctx, "height", 58, 48);
    } else if (animation.type === "probability_bag") {
      ctx.fillStyle = "#f7fbff";
      ctx.beginPath();
      ctx.moveTo(182, 58);
      ctx.quadraticCurveTo(160, 140, 192, 214);
      ctx.lineTo(326, 214);
      ctx.quadraticCurveTo(358, 140, 336, 58);
      ctx.closePath();
      ctx.fill();

      const balls = [
        { x: 222, y: 112, color: "#ff6b6b" },
        { x: 262, y: 96, color: "#4dabf7" },
        { x: 302, y: 116, color: "#51cf66" },
        { x: 242, y: 148, color: "#ffd43b" },
        { x: 286, y: 154, color: "#f783ac" },
      ];
      balls.forEach((ball, index) => {
        const lift = index === Math.floor(progress * balls.length) ? -42 * Math.sin(progress * Math.PI) : 0;
        ctx.fillStyle = ball.color;
        ctx.beginPath();
        ctx.arc(ball.x, ball.y + lift, 16, 0, Math.PI * 2);
        ctx.fill();
      });

      drawCanvasLabel(ctx, "one outcome is selected each time", 20, 226);
      drawCanvasLabel(ctx, "probability = favorable / total", 500, 226, "right");
    } else if (animation.type === "shop_percentages") {
      const bars = [
        { label: "Cost", value: 0.58, color: "#8ecae6" },
        { label: "Sell", value: 0.78 + 0.1 * Math.sin(progress * Math.PI * 2), color: "#90be6d" },
        { label: "Discount", value: 0.34 + 0.08 * Math.cos(progress * Math.PI * 2), color: "#f94144" },
      ];
      bars.forEach((bar, index) => {
        const x = 110 + index * 110;
        const barHeight = 120 * bar.value;
        ctx.fillStyle = bar.color;
        ctx.fillRect(x, 188 - barHeight, 54, barHeight);
        drawCanvasLabel(ctx, bar.label, x + 27, 208, "center");
      });
      drawCanvasLabel(ctx, "watch how the reference value changes before profit or loss is judged", 24, 30);
    } else if (animation.type === "field_lines") {
      ctx.fillStyle = "#ff9f1c";
      ctx.beginPath();
      ctx.arc(180, 130, 16, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = "#4cc9f0";
      ctx.beginPath();
      ctx.arc(340, 130, 16, 0, Math.PI * 2);
      ctx.fill();

      ctx.strokeStyle = "rgba(255,255,255,0.4)";
      for (let i = 0; i < 8; i += 1) {
        const offset = i * 14 - 48;
        ctx.beginPath();
        ctx.moveTo(196, 130 + offset);
        ctx.bezierCurveTo(240, 92 + offset * 0.3, 280, 92 + offset * 0.3, 324, 130 + offset);
        ctx.stroke();
      }
      drawCanvasLabel(ctx, "space itself carries the influence", 24, 30);
    } else if (animation.type === "concept_flow") {
      const nodes = [
        { x: 110, y: 130, label: "Cause", color: "#60a5fa" },
        { x: 260, y: 88, label: "Rule", color: "#7dd3fc" },
        { x: 410, y: 150, label: "Effect", color: "#fbbf24" },
      ];
      ctx.strokeStyle = "rgba(219, 234, 254, 0.48)";
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(nodes[0].x + 20, nodes[0].y);
      ctx.lineTo(nodes[1].x - 20, nodes[1].y);
      ctx.lineTo(nodes[2].x - 20, nodes[2].y);
      ctx.stroke();
      nodes.forEach((node, index) => {
        const bobble = Math.sin(progress * Math.PI * 2 + index * 0.8) * 6;
        ctx.fillStyle = node.color;
        ctx.beginPath();
        ctx.arc(node.x, node.y + bobble, 22, 0, Math.PI * 2);
        ctx.fill();
        drawCanvasLabel(ctx, node.label, node.x, node.y + bobble + 42, "center");
      });
      drawCanvasLabel(ctx, "connect the starting point, the rule, and the result", 24, 30);
    } else {
      const nodes = [
        { x: 110, y: 130, label: "Cause" },
        { x: 260, y: 88, label: "Rule" },
        { x: 410, y: 150, label: "Effect" },
      ];
      ctx.strokeStyle = "rgba(255,255,255,0.45)";
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(nodes[0].x, nodes[0].y);
      ctx.lineTo(nodes[1].x, nodes[1].y);
      ctx.lineTo(nodes[2].x, nodes[2].y);
      ctx.stroke();
      nodes.forEach((node, index) => {
        ctx.fillStyle = index === Math.floor(progress * nodes.length) ? "#ffd166" : "#f1f5f9";
        ctx.beginPath();
        ctx.arc(node.x, node.y, 22, 0, Math.PI * 2);
        ctx.fill();
        drawCanvasLabel(ctx, node.label, node.x, node.y + 42, "center");
      });
    }

    activeConceptAnimation = window.requestAnimationFrame(drawScene);
  };

  activeConceptAnimation = window.requestAnimationFrame(drawScene);
}

function renderAdaptiveProfile(profile) {
  if (!adaptiveProfileNote) {
    return;
  }
  if (!profile) {
    adaptiveProfileNote.textContent = "Challenge and teaching speed will adapt gradually as your accuracy, consistency, and behavior pattern evolve.";
    return;
  }
  adaptiveProfileNote.textContent = `Current adaptive mode: ${profile.question_difficulty} difficulty, ${profile.concept_depth} concept depth, ${profile.teaching_speed} teaching speed, ${String(profile.percentile_band || "").split("_").join(" ")}.`;
}

function renderReasoningPanel(video) {
  if (!reasoningPanel) {
    return;
  }

  reasoningPanel.innerHTML = "";
  if (!video) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = "Reasoning and calculations will appear here when the tutor explains a concept.";
    reasoningPanel.appendChild(empty);
    return;
  }

  const heading = document.createElement("h3");
  heading.textContent = "Reasoning And Calculations";
  reasoningPanel.appendChild(heading);

  const reasoningList = document.createElement("div");
  reasoningList.className = "reasoning-list";
  (video.reasoning || []).forEach((item) => {
    const line = document.createElement("div");
    line.className = "reasoning-card";
    line.textContent = item;
    reasoningList.appendChild(line);
  });
  reasoningPanel.appendChild(reasoningList);

  const calcHeading = document.createElement("p");
  calcHeading.className = "memory-heading";
  calcHeading.textContent = "Calculation flow";
  reasoningPanel.appendChild(calcHeading);

  const calcList = document.createElement("div");
  calcList.className = "reasoning-list";
  (video.calculations || []).forEach((item) => {
    const line = document.createElement("div");
    line.className = "reasoning-card";
    line.textContent = item;
    calcList.appendChild(line);
  });
  reasoningPanel.appendChild(calcList);
}

function clearVideoTimer() {
  if (activeVideoTimer) {
    window.clearInterval(activeVideoTimer);
    activeVideoTimer = null;
  }
}

function stopLessonNarration(keepCaption = false) {
  clearVideoTimer();
  if (supportsSpeech()) {
    window.speechSynthesis.cancel();
  }
  if (activeLessonNarration) {
    activeLessonNarration.cancelled = true;
    activeLessonNarration = null;
    }
    if (!keepCaption) {
      setAvatarStatusText("Ready");
      stopTalkingFace();
    }
}

function startLessonNarration(video, paintScene) {
  const scenes = (video && video.scenes) || [];
  if (!scenes.length) {
    return;
  }

  stopLessonNarration(true);
  const controller = { cancelled: false };
  activeLessonNarration = controller;
  let sceneIndex = 0;

  const speakScene = () => {
    if (controller.cancelled) {
      return;
    }
      if (sceneIndex >= scenes.length) {
        activeLessonNarration = null;
        setAvatarStatusText("Ready");
        stopTalkingFace();
        return;
      }

    const scene = scenes[sceneIndex];
    paintScene(sceneIndex);
    setCaption(scene.subtitle || "");

    if (!supportsSpeech()) {
      sceneIndex += 1;
      activeVideoTimer = window.setTimeout(speakScene, 2400);
      return;
    }

    const utterance = new SpeechSynthesisUtterance(scene.subtitle || "");
    const avatar = activeAvatar || avatarPresets[0] || null;
    const chosenVoice = findVoiceForAvatar(avatar);
    if (chosenVoice) {
      utterance.voice = chosenVoice;
    }
      utterance.rate = ((avatar && avatar.voice_rate) || 0.96) * 0.94;
      utterance.pitch = (avatar && avatar.voice_pitch) || 1.0;
      setAvatarStatusText("Explaining Live");
      updateTalkingFace(1);

    utterance.onboundary = (event) => {
      const index = typeof event.charIndex === "number" ? event.charIndex : 0;
      updateTalkingFace((Math.floor(index / 5) % 3) + 1);
    };
    utterance.onend = () => {
      if (controller.cancelled) {
        return;
      }
      sceneIndex += 1;
      window.setTimeout(speakScene, 180);
    };
    utterance.onerror = () => {
      if (controller.cancelled) {
        return;
      }
      sceneIndex += 1;
      window.setTimeout(speakScene, 180);
    };

    window.speechSynthesis.speak(utterance);
  };

  speakScene();
}

function renderVideoExplanation(video) {
  if (!videoExplanationPanel) {
    return;
  }

  stopLessonNarration();
  videoExplanationPanel.innerHTML = "";
  activeVideoExplanation = video;
  if (!video) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = "Ask for a concept and the lesson video storyboard will appear here.";
    videoExplanationPanel.appendChild(empty);
    return;
  }

  setActiveStudioPane("videoExplanationPanel");

  const title = document.createElement("h3");
  title.textContent = video.title;
  const languageTag = document.createElement("p");
  languageTag.className = "memory-heading";
  languageTag.textContent = `Subtitle language: ${video.subtitle_language}`;

  const controls = document.createElement("div");
  controls.className = "video-controls";
  const playAudioBtn = document.createElement("button");
  playAudioBtn.type = "button";
  playAudioBtn.className = "ghost-button";
  playAudioBtn.textContent = "Play lesson audio";
  const stopAudioBtn = document.createElement("button");
  stopAudioBtn.type = "button";
  stopAudioBtn.className = "ghost-button";
  stopAudioBtn.textContent = "Stop lesson audio";
  controls.appendChild(playAudioBtn);
  controls.appendChild(stopAudioBtn);

  const frame = document.createElement("div");
  frame.className = "video-stage";
  const sceneLabel = document.createElement("p");
  sceneLabel.className = "video-scene-label";
  const subtitle = document.createElement("p");
  subtitle.className = "video-subtitle";
  frame.appendChild(sceneLabel);
  frame.appendChild(subtitle);

  videoExplanationPanel.appendChild(title);
  videoExplanationPanel.appendChild(languageTag);
  videoExplanationPanel.appendChild(controls);
  videoExplanationPanel.appendChild(frame);

  const scenes = video.scenes || [];
  if (!scenes.length) {
    subtitle.textContent = "No scenes available yet.";
    return;
  }

  let sceneIndex = 0;
  const paintScene = (index = sceneIndex) => {
    const scene = scenes[index];
    sceneLabel.textContent = scene.label || `Scene ${index + 1}`;
    subtitle.textContent = scene.subtitle || "";
    if (autoCaptionMode.checked) {
      setCaption(scene.subtitle || "");
    }
    sceneIndex = (index + 1) % scenes.length;
  };
  paintScene();

  playAudioBtn.addEventListener("click", () => startLessonNarration(video, paintScene));
  stopAudioBtn.addEventListener("click", () => stopLessonNarration());

  if (scenes.length > 1) {
    activeVideoTimer = window.setInterval(paintScene, 2600);
  }

  if (autoSpeakReplies.checked) {
    startLessonNarration(video, paintScene);
  }
}

function getFeedForMode(mode) {
  if (mode === "guide") {
    return guideFeed;
  }
  if (mode === "lounge") {
    return loungeFeed;
  }
  if (mode === "practice") {
    return practiceFeed;
  }
  if (mode === "last_minute") {
    return lastMinuteFeed;
  }
  if (mode === "tips") {
    return tipsFeed;
  }
  return chatFeed;
}

function getDefaultFeedMessage(mode) {
  if (mode === "lounge") {
    return "This space is for casual talk, not pressure. We can chat first and study later.";
  }
  if (mode === "practice") {
    return "Ask for quick drills, PYQ-style questions, timed sets, or a full mini paper and I will keep the focus strictly on practice.";
  }
  return "Ask for explanations, quizzes, recovery support, or just start talking. I will help from wherever you are.";
}

function resetFeed(mode) {
  const feed = getFeedForMode(mode);
  if (!feed) {
    return;
  }
  feed.innerHTML = "";
  appendMessage(mode, "tutor", getDefaultFeedMessage(mode));
  if (mode === "tutor" && tutorRoomTranscriptFeed) {
    tutorRoomTranscriptFeed.innerHTML = "";
    appendFeedMessage(tutorRoomTranscriptFeed, mode, "tutor", getDefaultFeedMessage(mode));
    clearTutorCheckpointWidget();
  }
}

function appendFeedMessage(feed, mode, role, text) {
  if (!feed) {
    return null;
  }
  const wrapper = document.createElement("div");
  wrapper.className = `message ${role}`;
  if (mode === "practice") {
    wrapper.classList.add("practice-message");
  }
  const paragraph = document.createElement("p");
  if (role === "tutor") {
    // MARKED RENDERING FIXED
    window.marked.setOptions({ breaks: true, gfm: true });
    paragraph.innerHTML = marked.parse(normalizeTutorMathText(text || ""));
  } else {
    paragraph.textContent = text;
  }
  wrapper.appendChild(paragraph);
  feed.appendChild(wrapper);
  feed.scrollTop = feed.scrollHeight;
  return paragraph;
}

function syncTutorRoomTranscript() {
  if (!tutorRoomTranscriptFeed || !chatFeed) {
    return;
  }
  tutorRoomTranscriptFeed.innerHTML = "";
  Array.from(chatFeed.children).forEach((node) => {
    tutorRoomTranscriptFeed.appendChild(node.cloneNode(true));
  });
  tutorRoomTranscriptFeed.scrollTop = tutorRoomTranscriptFeed.scrollHeight;
}

function renderTutorConversations(conversations) {
  if (!tutorConversationList) {
    return;
  }
  tutorConversationSnapshot = sortTutorConversations(Array.isArray(conversations) ? conversations : []);
  tutorConversationList.innerHTML = "";
  const previewConversations = tutorConversationSnapshot.slice(0, 3);
  if (!previewConversations.length) {
    tutorConversationList.innerHTML = `<p class="muted">No saved tutor chats yet. Click "New chat" to start one.</p>`;
    renderTutorConversationDrawer();
    return;
  }

  previewConversations.forEach((conversation) => {
    tutorConversationList.appendChild(buildTutorConversationRow(conversation, { includeDelete: false }));
  });
  renderTutorConversationDrawer();
}

function renderDeletedTutorConversations(conversations) {

  if (!deletedTutorConversationList) {
    return;
  }
  deletedTutorConversationList.innerHTML = "";
  if (!conversations || !conversations.length) {
    deletedTutorConversationList.innerHTML = `<p class="muted">Deleted tutor chats will appear here when available.</p>`;
    return;
  }

  conversations.forEach((conversation) => {
    const row = document.createElement("div");
    row.className = "conversation-row deleted";

    const copy = document.createElement("div");
    copy.className = "conversation-copy";

    const title = document.createElement("strong");
    title.textContent = conversation.title || "Deleted chat";
    const meta = document.createElement("span");
    meta.className = "conversation-meta";
    meta.textContent = conversation.deleted_at || conversation.updated_at || "";
    copy.appendChild(title);
    copy.appendChild(meta);

    const restoreButton = document.createElement("button");
    restoreButton.type = "button";
    restoreButton.className = "ghost-button";
    restoreButton.textContent = "Restore";
    restoreButton.addEventListener("click", async () => {
      await restoreTutorConversation(conversation.id);
    });

    row.appendChild(copy);
    row.appendChild(restoreButton);
    deletedTutorConversationList.appendChild(row);
  });
}

function buildTutorConversationRow(conversation, { includeDelete = false } = {}) {
  const row = document.createElement("div");
  row.className = `conversation-row${Number(conversation.id) === Number(activeTutorConversationId) ? " active" : ""}`;

  const copy = document.createElement("div");
  copy.className = "conversation-copy";

  const openButton = document.createElement("button");
  openButton.type = "button";
  openButton.className = "conversation-open";
  openButton.textContent = `${conversation.pinned_at ? "Pinned: " : ""}${conversation.title || "New chat"}`;
  openButton.addEventListener("click", async () => {
    activeTutorConversationId = conversation.id;
    renderTutorConversations(tutorConversationSnapshot);
    await fetchChatHistory("tutor", activeTutorConversationId);
  });

  const meta = document.createElement("span");
  meta.className = "conversation-meta";
  meta.textContent = conversation.updated_at || "";

  copy.appendChild(openButton);
  copy.appendChild(meta);

  const actions = document.createElement("div");
  actions.className = "conversation-actions";

  const renameButton = document.createElement("button");
  renameButton.type = "button";
  renameButton.className = "ghost-button conversation-icon-button";
  renameButton.textContent = "\u270E";
  renameButton.title = "Rename";
  renameButton.setAttribute("aria-label", "Rename");
  renameButton.addEventListener("click", async () => {
    const nextTitle = window.prompt("Rename this chat", conversation.title || "New chat");
    if (nextTitle === null) {
      return;
    }
    await updateTutorConversation(conversation.id, { title: nextTitle });
  });

  const pinButton = document.createElement("button");
  pinButton.type = "button";
  pinButton.className = "ghost-button conversation-icon-button";
  pinButton.textContent = conversation.pinned_at ? "\u{1F4CC}" : "\u{1F4CD}";
  pinButton.title = conversation.pinned_at ? "Unpin" : "Pin";
  pinButton.setAttribute("aria-label", conversation.pinned_at ? "Unpin" : "Pin");
  pinButton.addEventListener("click", async () => {
    await updateTutorConversation(conversation.id, { pinned: !conversation.pinned_at });
  });

  actions.appendChild(renameButton);
  actions.appendChild(pinButton);

  if (includeDelete) {
    const deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.className = "ghost-button conversation-icon-button danger";
    deleteButton.textContent = "\u{1F5D1}";
    deleteButton.title = "Delete";
    deleteButton.setAttribute("aria-label", "Delete");
    deleteButton.addEventListener("click", async () => {
      await deleteTutorConversation(conversation.id);
    });
    actions.appendChild(deleteButton);
  }

  row.appendChild(copy);
  row.appendChild(actions);
  return row;
}

async function deleteTutorConversation(conversationId) {
  if (!activeProfile || !activeProfile.name || !conversationId) {
    return;
  }
  const response = await fetch("/api/chat-history/delete", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      student_name: activeProfile.name,
      conversation_mode: "tutor",
      conversation_id: conversationId,
    }),
  });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || "Could not delete that chat.");
  }
  activeTutorConversationId = payload.conversations && payload.conversations.length ? payload.conversations[0].id : null;
  tutorConversationSnapshot = payload.conversations || [];
  deletedTutorConversationSnapshot = payload.deleted_conversations || [];
  renderTutorConversations(tutorConversationSnapshot);
  renderDeletedTutorConversations(deletedTutorConversationSnapshot);
  if (activeTutorConversationId) {
    await fetchChatHistory("tutor", activeTutorConversationId);
  } else {
    resetFeed("tutor");
  }
  renderStorageStatus(payload.storage_status || null);
}

function sortTutorConversations(conversations = []) {
  return [...conversations].sort((left, right) => {
    const leftPinned = left && left.pinned_at ? 1 : 0;
    const rightPinned = right && right.pinned_at ? 1 : 0;
    if (leftPinned !== rightPinned) {
      return rightPinned - leftPinned;
    }
    const leftTime = new Date(left && (left.updated_at || left.created_at || 0)).getTime() || 0;
    const rightTime = new Date(right && (right.updated_at || right.created_at || 0)).getTime() || 0;
    if (rightTime !== leftTime) {
      return rightTime - leftTime;
    }
    return String(right && right.title || "").localeCompare(String(left && left.title || ""));
  });
}

function getTutorConversationBucket(conversation) {
  const timeText = conversation && (conversation.updated_at || conversation.created_at || conversation.deleted_at || "");
  const time = new Date(timeText);
  if (Number.isNaN(time.getTime())) {
    return "Older";
  }
  const now = new Date();
  const startOfToday = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const startOfTarget = new Date(time.getFullYear(), time.getMonth(), time.getDate());
  const diffDays = Math.floor((startOfToday.getTime() - startOfTarget.getTime()) / 86400000);
  if (diffDays <= 0) {
    return "Today";
  }
  if (diffDays === 1) {
    return "Yesterday";
  }
  if (diffDays <= 7) {
    return "This Week";
  }
  return "Older";
}

function renderTutorConversationDrawer() {
  if (!tutorConversationDrawer) {
    return;
  }
  if (tutorConversationDrawer.classList.contains("hidden")) {
    return;
  }

  const buckets = {
    Today: tutorConversationDrawerToday,
    Yesterday: tutorConversationDrawerYesterday,
    "This Week": tutorConversationDrawerWeek,
    Older: tutorConversationDrawerOlder,
  };
  Object.values(buckets).forEach((container) => {
    if (container) {
      container.innerHTML = "";
    }
  });

  const conversations = sortTutorConversations(tutorConversationSnapshot);
  if (!conversations.length) {
    if (tutorConversationDrawerToday) {
      tutorConversationDrawerToday.innerHTML = `<p class="muted">No saved tutor chats yet.</p>`;
    }
  } else {
    conversations.forEach((conversation) => {
      const bucketName = getTutorConversationBucket(conversation);
      const container = buckets[bucketName] || tutorConversationDrawerOlder;
      if (!container) {
        return;
      }
      container.appendChild(buildTutorConversationRow(conversation, { includeDelete: true }));
    });
  }

  renderDeletedTutorConversations(deletedTutorConversationSnapshot);
}

function openTutorConversationDrawer() {
  if (!tutorConversationDrawer) {
    return;
  }
  tutorConversationDrawer.classList.remove("hidden");
  tutorConversationDrawer.setAttribute("aria-hidden", "false");
  if (tutorConversationDrawerBackdrop) {
    tutorConversationDrawerBackdrop.classList.remove("hidden");
  }
  renderTutorConversationDrawer();
}

function closeTutorConversationDrawer() {
  if (tutorConversationDrawer) {
    tutorConversationDrawer.classList.add("hidden");
    tutorConversationDrawer.setAttribute("aria-hidden", "true");
  }
  if (tutorConversationDrawerBackdrop) {
    tutorConversationDrawerBackdrop.classList.add("hidden");
  }
}

function formatLoungeConversationLabel(conversation) {
  const title = conversation && conversation.title ? conversation.title : "New chat";
  const pinned = conversation && conversation.pinned_at ? "Pinned - " : "";
  return `${pinned}${title}`;
}

function getSelectedLoungeConversation() {
  return loungeConversationSnapshot.find((conversation) => Number(conversation.id) === Number(activeLoungeConversationId)) || null;
}

function getSelectedDeletedLoungeConversation() {
  const selectedId = deletedLoungeConversationSelect ? Number(deletedLoungeConversationSelect.value) : NaN;
  return deletedLoungeConversationSnapshot.find((conversation) => Number(conversation.id) === selectedId) || null;
}

function setLoungePopover(panel, toggle, open) {
  if (!panel || !toggle) {
    return;
  }
  panel.classList.toggle("hidden", !open);
  toggle.setAttribute("aria-expanded", open ? "true" : "false");
  if (panel === loungeHistoryPanel) {
    panel.setAttribute("aria-hidden", open ? "false" : "true");
  }
}

function closeLoungePanels() {
  setLoungePopover(loungeTimerPanel, loungeTimerToggleBtn, false);
  setLoungePopover(loungeHistoryPanel, loungeHistoryToggleBtn, false);
}

function setLoungeActionState(conversation) {
  const disabled = !conversation;
  [loungeRenameChatBtn, loungePinChatBtn, loungeDeleteChatBtn].forEach((button) => {
    if (button) {
      button.disabled = disabled;
    }
  });
  if (loungePinChatBtn) {
    loungePinChatBtn.textContent = conversation && conversation.pinned_at ? "Unpin" : "Pin";
  }
}

function renderLoungeConversations(conversations) {
  loungeConversationSnapshot = Array.isArray(conversations) ? conversations : [];
  if (!loungeConversationList || !loungeConversationSelect) {
    return;
  }

  loungeConversationSelect.innerHTML = "";
  if (!loungeConversationSnapshot.length) {
    const option = document.createElement("option");
    option.value = "";
    option.textContent = "No saved lounge chats yet";
    loungeConversationSelect.appendChild(option);
    loungeConversationSelect.disabled = true;
    activeLoungeConversationId = null;
    setLoungeActionState(null);
    return;
  }

  const activeStillExists = loungeConversationSnapshot.some((conversation) => Number(conversation.id) === Number(activeLoungeConversationId));
  if (!activeStillExists) {
    activeLoungeConversationId = loungeConversationSnapshot[0].id;
  }

  loungeConversationSnapshot.forEach((conversation) => {
    const option = document.createElement("option");
    option.value = String(conversation.id);
    option.textContent = formatLoungeConversationLabel(conversation);
    option.selected = Number(conversation.id) === Number(activeLoungeConversationId);
    loungeConversationSelect.appendChild(option);
  });
  loungeConversationSelect.disabled = false;
  setLoungeActionState(getSelectedLoungeConversation());
}

function renderDeletedLoungeConversations(conversations) {
  deletedLoungeConversationSnapshot = Array.isArray(conversations) ? conversations : [];
  if (!deletedLoungeConversationList || !deletedLoungeConversationSelect) {
    return;
  }

  deletedLoungeConversationSelect.innerHTML = "";
  if (!deletedLoungeConversationSnapshot.length) {
    const option = document.createElement("option");
    option.value = "";
    option.textContent = "No deleted lounge chats";
    deletedLoungeConversationSelect.appendChild(option);
    deletedLoungeConversationSelect.disabled = true;
    if (restoreLoungeChatBtn) {
      restoreLoungeChatBtn.disabled = true;
    }
    return;
  }

  deletedLoungeConversationSnapshot.forEach((conversation, index) => {
    const option = document.createElement("option");
    option.value = String(conversation.id);
    option.textContent = formatLoungeConversationLabel({
      ...conversation,
      updated_at: conversation.deleted_at || conversation.updated_at || "",
    });
    option.selected = index === 0;
    deletedLoungeConversationSelect.appendChild(option);
  });
  deletedLoungeConversationSelect.disabled = false;
  if (restoreLoungeChatBtn) {
    restoreLoungeChatBtn.disabled = false;
  }
}
function renderChatHistory(mode, messages) {
  const feed = getFeedForMode(mode);
  if (!feed) {
    return;
  }
  feed.innerHTML = "";
  if (mode === "tutor" && tutorRoomTranscriptFeed) {
    tutorRoomTranscriptFeed.innerHTML = "";
  }
  if (!messages || !messages.length) {
    appendMessage(mode, "tutor", getDefaultFeedMessage(mode));
    return;
  }
  messages.forEach((message) => {
    appendMessage(mode, message.role === "student" ? "student" : "tutor", message.message_text || "");
  });
}

async function fetchChatHistory(mode, conversationId = null) {
  if (!activeProfile || !activeProfile.name) {
    return;
  }
  const query = new URLSearchParams({ conversation_mode: mode });
  if (conversationId) {
    query.set("conversation_id", String(conversationId));
  }
  const response = await fetch(`/api/chat-history/${encodeURIComponent(activeProfile.name)}?${query.toString()}`);
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || "Could not load saved chat history.");
  }
  if (mode === "tutor" && payload.conversation_id) {
    activeTutorConversationId = payload.conversation_id;
  } else if (mode === "lounge" && payload.conversation_id) {
    activeLoungeConversationId = payload.conversation_id;
  }
  renderChatHistory(mode, payload.messages || []);
}

async function deleteChatHistory(mode) {
  if (!activeProfile || !activeProfile.name) {
    return;
  }
  const response = await fetch("/api/chat-history/delete", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      student_name: activeProfile.name,
      conversation_mode: mode,
      conversation_id: mode === "tutor" ? activeTutorConversationId : mode === "lounge" ? activeLoungeConversationId : null,
    }),
  });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || "Could not delete that chat.");
  }
  if (mode === "tutor") {
    activeTutorConversationId = null;
    renderTutorConversations(payload.conversations || []);
    renderDeletedTutorConversations(payload.deleted_conversations || []);
    if (payload.conversations && payload.conversations.length) {
      activeTutorConversationId = payload.conversations[0].id;
      await fetchChatHistory("tutor", activeTutorConversationId);
    } else {
      resetFeed("tutor");
    }
  } else if (mode === "lounge") {
    activeLoungeConversationId = null;
    renderLoungeConversations(payload.conversations || []);
    renderDeletedLoungeConversations(payload.deleted_conversations || []);
    if (payload.conversations && payload.conversations.length) {
      activeLoungeConversationId = payload.conversations[0].id;
      await fetchChatHistory("lounge", activeLoungeConversationId);
    } else {
      resetFeed("lounge");
    }
  } else {
    resetFeed(mode);
  }
  renderStorageStatus(payload.storage_status || null);
}

async function fetchTutorConversations(selectConversationId = null) {
  if (!activeProfile || !activeProfile.name) {
    renderTutorConversations([]);
    return;
  }
  const query = new URLSearchParams({ conversation_mode: "tutor" });
  if (tutorConversationSearch) {
    query.set("q", tutorConversationSearch);
  }
  const response = await fetch(`/api/conversations/${encodeURIComponent(activeProfile.name)}?${query.toString()}`);
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || "Could not load tutor chats.");
  }
  const conversations = payload.conversations || [];
  if (selectConversationId) {
    activeTutorConversationId = selectConversationId;
  } else if (!activeTutorConversationId && conversations.length) {
    activeTutorConversationId = conversations[0].id;
  }
  renderTutorConversations(conversations);
  if (activeTutorConversationId) {
    await fetchChatHistory("tutor", activeTutorConversationId);
  } else {
    resetFeed("tutor");
  }
  await fetchDeletedTutorConversations();
}

async function fetchConversationsByMode(mode, searchQuery = "") {
  if (!activeProfile || !activeProfile.name) {
    return [];
  }
  const query = new URLSearchParams({ conversation_mode: mode });
  if (searchQuery) {
    query.set("q", searchQuery);
  }
  const response = await fetch(`/api/conversations/${encodeURIComponent(activeProfile.name)}?${query.toString()}`);
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || `Could not load ${mode} chats.`);
  }
  return payload.conversations || [];
}

async function fetchDeletedConversationsByMode(mode) {
  if (!activeProfile || !activeProfile.name) {
    return [];
  }
  const response = await fetch(`/api/conversations/deleted/${encodeURIComponent(activeProfile.name)}?conversation_mode=${encodeURIComponent(mode)}`);
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || `Could not load deleted ${mode} chats.`);
  }
  return payload.conversations || [];
}

async function createTutorConversation() {
  if (!activeProfile || !activeProfile.name) {
    return;
  }
  const response = await fetch("/api/conversations/new", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      student_name: activeProfile.name,
      conversation_mode: "tutor",
      title: "New chat",
    }),
  });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || "Could not create a new chat.");
  }
  activeTutorConversationId = payload.conversation ? payload.conversation.id : null;
  renderTutorConversations(payload.conversations || []);
  resetFeed("tutor");
  await fetchDeletedTutorConversations();
}

async function fetchLoungeConversations(selectConversationId = null) {
  if (!activeProfile || !activeProfile.name) {
    renderLoungeConversations([]);
    return;
  }
  const conversations = await fetchConversationsByMode("lounge", loungeConversationSearch);
  if (selectConversationId) {
    activeLoungeConversationId = selectConversationId;
  } else if (!activeLoungeConversationId && conversations.length) {
    activeLoungeConversationId = conversations[0].id;
  }
  renderLoungeConversations(conversations);
  if (activeLoungeConversationId) {
    await fetchChatHistory("lounge", activeLoungeConversationId);
  } else {
    resetFeed("lounge");
  }
  renderDeletedLoungeConversations(await fetchDeletedConversationsByMode("lounge"));
}

async function createLoungeConversation() {
  if (!activeProfile || !activeProfile.name) {
    return;
  }
  const response = await fetch("/api/conversations/new", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      student_name: activeProfile.name,
      conversation_mode: "lounge",
      title: "New chat",
    }),
  });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || "Could not create a new lounge chat.");
  }
  activeLoungeConversationId = payload.conversation ? payload.conversation.id : null;
  renderLoungeConversations(payload.conversations || []);
  resetFeed("lounge");
  renderDeletedLoungeConversations(await fetchDeletedConversationsByMode("lounge"));
}

async function fetchDeletedTutorConversations() {
  if (!activeProfile || !activeProfile.name) {
    deletedTutorConversationSnapshot = [];
    renderDeletedTutorConversations([]);
    return;
  }
  const response = await fetch(`/api/conversations/deleted/${encodeURIComponent(activeProfile.name)}?conversation_mode=tutor`);
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || "Could not load deleted tutor chats.");
  }
  deletedTutorConversationSnapshot = payload.conversations || [];
  renderDeletedTutorConversations(deletedTutorConversationSnapshot);
}

async function restoreTutorConversation(conversationId) {
  if (!activeProfile || !activeProfile.name) {
    return;
  }
  const response = await fetch("/api/conversations/restore", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      student_name: activeProfile.name,
      conversation_mode: "tutor",
      conversation_id: conversationId,
    }),
  });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || "Could not restore that chat.");
  }
  activeTutorConversationId = conversationId;
  renderTutorConversations(payload.conversations || []);
  renderDeletedTutorConversations(payload.deleted_conversations || []);
  await fetchChatHistory("tutor", activeTutorConversationId);
}

async function updateTutorConversation(conversationId, updates) {
  await updateConversationByMode("tutor", conversationId, updates);
}

async function updateConversationByMode(mode, conversationId, updates) {
  if (!activeProfile || !activeProfile.name) {
    return;
  }
  const response = await fetch("/api/conversations/update", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      student_name: activeProfile.name,
      conversation_mode: mode,
      conversation_id: conversationId,
      title: Object.prototype.hasOwnProperty.call(updates, "title") ? updates.title : null,
      pinned: Object.prototype.hasOwnProperty.call(updates, "pinned") ? updates.pinned : null,
    }),
  });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || "Could not update that chat.");
  }
  if (mode === "tutor") {
    renderTutorConversations(payload.conversations || []);
    renderDeletedTutorConversations(payload.deleted_conversations || []);
  } else if (mode === "lounge") {
    renderLoungeConversations(payload.conversations || []);
    renderDeletedLoungeConversations(payload.deleted_conversations || []);
  }
}

async function restoreConversationByMode(mode, conversationId) {
  if (!activeProfile || !activeProfile.name) {
    return;
  }
  const response = await fetch("/api/conversations/restore", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      student_name: activeProfile.name,
      conversation_mode: mode,
      conversation_id: conversationId,
    }),
  });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || "Could not restore that chat.");
  }
  if (mode === "tutor") {
    activeTutorConversationId = conversationId;
    renderTutorConversations(payload.conversations || []);
    renderDeletedTutorConversations(payload.deleted_conversations || []);
    await fetchChatHistory("tutor", activeTutorConversationId);
  } else if (mode === "lounge") {
    activeLoungeConversationId = conversationId;
    renderLoungeConversations(payload.conversations || []);
    renderDeletedLoungeConversations(payload.deleted_conversations || []);
    await fetchChatHistory("lounge", activeLoungeConversationId);
  }
}

function renderStorageStatus(status) {
  if (!dataSaveStatus || !dataSaveCounts) {
    return;
  }
  if (!status) {
    dataSaveStatus.textContent = "Your progress, settings, and chats are saved automatically.";
    dataSaveCounts.textContent = "Saved data will appear after your profile loads.";
    return;
  }
  dataSaveStatus.textContent = status.profile_saved
    ? "Your progress, settings, and chats are saved automatically."
    : "Your profile has not been saved yet.";
  const savedParts = [];
  if (status.progress_items) savedParts.push(`${status.progress_items} progress items`);
  if (status.chat_messages) savedParts.push(`${status.chat_messages} chat messages`);
  if (status.syllabus_documents) savedParts.push(`${status.syllabus_documents} syllabus docs`);
  dataSaveCounts.textContent = savedParts.length ? savedParts.join(" | ") : "Astra will start saving once you study.";
}

async function fetchStorageStatus(studentName) {
  if (!studentName) {
    renderStorageStatus(null);
    return;
  }
  const response = await fetch(`/api/storage-status/${encodeURIComponent(studentName)}`);
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || "Could not load saved-data status.");
  }
  renderStorageStatus(payload);
}

function renderTutorVideoBridge(video) {
  if (!tutorVideoBridgeCues) {
    return;
  }

  tutorVideoBridgeCues.innerHTML = "";
  if (!video) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = "Choose a tutor video to see its 3D bridge, cue points, and lesson flow.";
    tutorVideoBridgeCues.appendChild(empty);
    return;
  }

  const cueGroups = [];
  if (video.match_reasons && video.match_reasons.length) {
    cueGroups.push(`Why it is ranked here: ${video.match_reasons.slice(0, 2).join(" ")}`);
  }
  if (video.visual_learning && video.visual_learning.scenario) {
    cueGroups.push(`3D scene: ${video.visual_learning.scenario}`);
  }
  const visualFrames = video.visual_learning && Array.isArray(video.visual_learning.frames) ? video.visual_learning.frames : [];
  if (visualFrames.length) {
    cueGroups.push(`First visual step: ${visualFrames[0]}`);
  }
  const calculationSteps = video.video_explanation && Array.isArray(video.video_explanation.calculations)
    ? video.video_explanation.calculations
    : [];
  if (calculationSteps.length) {
    cueGroups.push(`First calculation step: ${calculationSteps[0]}`);
  }
  if (Array.isArray(video.cue_points) && video.cue_points.length) {
    cueGroups.push(`Creator cue: ${video.cue_points[0]}`);
  }

  if (!cueGroups.length) {
    cueGroups.push("This video can be used to seed a Tutor explanation and a 3D concept board.");
  }

  cueGroups.forEach((cue) => {
    const item = document.createElement("p");
    item.className = "video-library-cue";
    item.textContent = cue;
    tutorVideoBridgeCues.appendChild(item);
  });
}

function renderVideoLibrary(snapshot) {
  videoLibrarySnapshot = snapshot || null;
  if (!tutorVideoList) {
    refreshVideoSearchResults();
    return;
  }

  tutorVideoList.innerHTML = "";
  if (!snapshot || !Array.isArray(snapshot.videos) || !snapshot.videos.length) {
    if (tutorVideoPlayer) {
      tutorVideoPlayer.removeAttribute("src");
      tutorVideoPlayer.load();
    }
    
if (openVideoBridgeBtn) {
      openVideoBridgeBtn.disabled = true;
    }
    if (useVideoInTutorBtn) {
      useVideoInTutorBtn.disabled = true;
    }
    activeTutorVideo = null;
    if (tutorVideoTitle) {
      tutorVideoTitle.textContent = "Welcome";
    }
    renderTutorVideoBridge(null);
    const mediaRoot = APP_CONFIG.video_library_media_root || "web/media/tutor-videos";
    const manifestPath = APP_CONFIG.video_library_manifest_path || "data/tutor_video_library.json";
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = `No tutor videos found yet. Drop mp4 or webm files into ${mediaRoot}, or add manifest entries in ${manifestPath}. They will appear inside the tutor room.`;
    tutorVideoList.appendChild(empty);
    return;
  }

  const videoItems = snapshot.videos;
  const selectedVideoId = activeTutorVideo && activeTutorVideo.id ? activeTutorVideo.id : "";
  const selectedVideo = videoItems.find((item) => item.id === selectedVideoId) || pickWelcomeTutorVideo(snapshot) || videoItems[0];
  activeTutorVideo = selectedVideo || null;

  if (tutorVideoPlayer && selectedVideo && selectedVideo.url) {
    tutorVideoPlayer.src = selectedVideo.url;
    tutorVideoPlayer.load();
    if (openVideoBridgeBtn) {
      openVideoBridgeBtn.disabled = false;
    }
    if (useVideoInTutorBtn) {
      useVideoInTutorBtn.disabled = false;
    }
  }
  if (tutorVideoTitle) {
    tutorVideoTitle.textContent = selectedVideo ? selectedVideo.title || "Welcome" : "Welcome";
  }

  videoItems.forEach((video) => {
    const card = document.createElement("button");
    card.type = "button";
    card.className = `video-library-item${selectedVideo && video.id === selectedVideo.id ? " active" : ""}`;
    card.addEventListener("click", () => {
      activeTutorVideo = video;
      if (video.url) {
        if (tutorVideoPlayer) {
          tutorVideoPlayer.src = video.url;
          tutorVideoPlayer.load();
          const playResult = tutorVideoPlayer.play();
          if (playResult && typeof playResult.catch === "function") {
            playResult.catch(() => {});
          }
        }
        if (tutorVideoTitle) {
          tutorVideoTitle.textContent = video.title || "Welcome";
        }
        openGeneratedVideoForTopic(video.topic || video.title || "Tutor Video", video.subject || "", video.url);
      } else {
        updateAstraCurrentTopic(video.topic || video.title || "", video.subject || "", "video_library");
      }
      renderVideoLibrary(videoLibrarySnapshot);
    });

    const info = document.createElement("div");
    info.className = "video-library-player-copy";
    const title = document.createElement("strong");
    title.className = "exam-chip-title";
    title.textContent = video.title || "Tutor Video";

    info.appendChild(title);
    card.appendChild(info);
    tutorVideoList.appendChild(card);
  });
  ensureWelcomeTutorVideoLoaded();
  renderVideoTutorSubjectItems(activeVideoSearchQuery);
}

function pickWelcomeTutorVideo(snapshot = null) {
  const videos = snapshot && Array.isArray(snapshot.videos) ? snapshot.videos : [];
  if (!videos.length) {
    return null;
  }
  return videos.find((video) => video.id === "welcome-back-female-tutor")
    || videos.find((video) => video.id === "female-homepage-hero")
    || videos.find((video) => String(video.title || "").toLowerCase().includes("welcome"))
    || videos.find((video) => (video.tags || []).some((tag) => String(tag || "").toLowerCase().includes("welcome")))
    || videos[0]
    || null;
}

function ensureWelcomeTutorVideoLoaded() {
  if (!videoLibrarySnapshot || !Array.isArray(videoLibrarySnapshot.videos) || !videoLibrarySnapshot.videos.length) {
    return;
  }
  if (activeTutorVideo && activeTutorVideo.url) {
    return;
  }
  const welcomeVideo = pickWelcomeTutorVideo(videoLibrarySnapshot);
  if (!welcomeVideo || !welcomeVideo.url) {
    return;
  }
  activeTutorVideo = welcomeVideo;
  if (tutorVideoPlayer) {
    tutorVideoPlayer.src = welcomeVideo.url;
    tutorVideoPlayer.load();
  }
  if (tutorVideoTitle) {
    tutorVideoTitle.textContent = welcomeVideo.title || "Welcome";
  }
  if (openVideoBridgeBtn) {
    openVideoBridgeBtn.disabled = false;
  }
  if (useVideoInTutorBtn) {
    useVideoInTutorBtn.disabled = false;
  }
}

function preferTutorVideosForAvatar(avatar) {
  if (!avatar || !videoLibrarySnapshot || !Array.isArray(videoLibrarySnapshot.videos) || !videoLibrarySnapshot.videos.length) {
    return;
  }

  const featuredIds = Array.isArray(avatar.featured_video_ids) ? avatar.featured_video_ids : [];
  if (!featuredIds.length) {
    return;
  }

  const featuredVideo = videoLibrarySnapshot.videos.find((video) => featuredIds.includes(video.id));
  if (!featuredVideo) {
    return;
  }

  activeTutorVideo = featuredVideo;
  renderVideoLibrary(videoLibrarySnapshot);
}

function pickAuthHeroVideo(snapshot) {
  if (!snapshot || !Array.isArray(snapshot.videos) || !snapshot.videos.length) {
    return null;
  }
  return snapshot.videos.find((video) => video.id === "female-homepage-hero")
    || snapshot.videos.find((video) => (video.tags || []).some((tag) => String(tag || "").toLowerCase().includes("homepage")))
    || snapshot.videos[0]
    || null;
}

function renderAuthHeroVideo(snapshot) {
  authHeroVideoSnapshot = snapshot || null;
  if (!authHeroVideoPlayer) {
    return;
  }

  const selectedVideo = pickAuthHeroVideo(snapshot);
  if (!selectedVideo) {
    authHeroVideoPlayer.removeAttribute("src");
    authHeroVideoPlayer.load();
    if (authHeroVideoTitle) {
      authHeroVideoTitle.textContent = "Homepage hero video";
    }
    if (authHeroVideoMeta) {
      authHeroVideoMeta.textContent = "A warm opening video will appear here when the library loads.";
    }
    if (authHeroVideoSummary) {
      authHeroVideoSummary.textContent = "This preview is intentionally subtle so it feels like part of the brand, not an interruption.";
    }
    if (authHeroVideoTag) {
      authHeroVideoTag.textContent = "Preview";
    }
    if (authHeroVideoToggle) {
      authHeroVideoToggle.textContent = "Play preview";
      authHeroVideoToggle.disabled = true;
    }
    return;
  }

  authHeroVideoPlayer.src = selectedVideo.url || "";
  authHeroVideoPlayer.muted = true;
  authHeroVideoPlayer.loop = true;
  authHeroVideoPlayer.playsInline = true;
  authHeroVideoPlayer.autoplay = true;
  authHeroVideoPlayer.load();
  const playPromise = authHeroVideoPlayer.play();
  if (playPromise && typeof playPromise.catch === "function") {
    playPromise.catch(() => {});
  }

  if (authHeroVideoTitle) {
    authHeroVideoTitle.textContent = selectedVideo.title || "Homepage hero video";
  }
  if (authHeroVideoMeta) {
    const metaParts = [];
    if (selectedVideo.topic) {
      metaParts.push(selectedVideo.topic);
    }
    if (selectedVideo.level) {
      metaParts.push(selectedVideo.level);
    }
    if (selectedVideo.duration_label) {
      metaParts.push(selectedVideo.duration_label);
    }
    authHeroVideoMeta.textContent = metaParts.length
      ? metaParts.join(" | ")
      : "Homepage welcome preview";
  }
  if (authHeroVideoSummary) {
    authHeroVideoSummary.textContent = selectedVideo.summary || "A warm opening video for the homepage.";
  }
  if (authHeroVideoTag) {
    authHeroVideoTag.textContent = selectedVideo.source_type === "local_file" ? "Local hero" : "Manifest hero";
  }
  if (authHeroVideoToggle) {
    authHeroVideoToggle.disabled = false;
    authHeroVideoToggle.textContent = "Pause preview";
  }
}

async function toggleAuthHeroVideoPlayback() {
  if (!authHeroVideoPlayer || authHeroVideoPlayer.disabled) {
    return;
  }
  if (authHeroVideoPlayer.paused) {
    try {
      await authHeroVideoPlayer.play();
    } catch (error) {
      console.warn("Could not play homepage hero video:", error);
      return;
    }
    if (authHeroVideoToggle) {
      authHeroVideoToggle.textContent = "Pause preview";
    }
    return;
  }
  authHeroVideoPlayer.pause();
  if (authHeroVideoToggle) {
    authHeroVideoToggle.textContent = "Play preview";
  }
}

function pickIntroVideo(snapshot, mode = "signin") {
  if (!snapshot || !Array.isArray(snapshot.videos) || !snapshot.videos.length) {
    return null;
  }
  if (mode === "signup") {
    return snapshot.videos.find((video) => video.id === "female-homepage-hero")
      || snapshot.videos.find((video) => (video.tags || []).some((tag) => String(tag || "").toLowerCase().includes("homepage")))
      || snapshot.videos[0]
      || null;
  }
  return snapshot.videos.find((video) => video.id === "welcome-back-female-tutor")
    || snapshot.videos.find((video) => (video.tags || []).some((tag) => String(tag || "").toLowerCase().includes("welcome")))
    || snapshot.videos[0]
    || null;
}

function renderIntroVideo(snapshot, mode = introVideoMode) {
  introVideoSnapshot = snapshot || null;
  if (!introVideoPlayer) {
    return;
  }

  const selectedVideo = pickIntroVideo(snapshot, mode);
  if (!selectedVideo) {
    introVideoPlayer.removeAttribute("src");
    introVideoPlayer.load();
    if (introVideoTitle) {
      introVideoTitle.textContent = "Welcome video";
    }
    if (introVideoMeta) {
      introVideoMeta.textContent = "Your Astra intro video will appear here after sign-in or sign-up.";
    }
    if (introVideoSummary) {
      introVideoSummary.textContent = "A calm, branded introduction that feels like part of the website flow.";
    }
    if (introVideoTag) {
      introVideoTag.textContent = "Intro";
    }
    if (introVideoToggle) {
      introVideoToggle.textContent = "Pause";
      introVideoToggle.disabled = true;
    }
    return;
  }

  introVideoPlayer.src = selectedVideo.url || "";
  introVideoPlayer.muted = true;
  introVideoPlayer.loop = true;
  introVideoPlayer.playsInline = true;
  introVideoPlayer.autoplay = true;
  introVideoPlayer.load();
  const playPromise = introVideoPlayer.play();
  if (playPromise && typeof playPromise.catch === "function") {
    playPromise.catch(() => {});
  }

  if (introVideoTitle) {
    introVideoTitle.textContent = selectedVideo.title || "Welcome video";
  }
  if (introVideoMeta) {
    const metaParts = [];
    if (selectedVideo.topic) metaParts.push(selectedVideo.topic);
    if (selectedVideo.level) metaParts.push(selectedVideo.level);
    if (selectedVideo.duration_label) metaParts.push(selectedVideo.duration_label);
    introVideoMeta.textContent = metaParts.length ? metaParts.join(" | ") : "Astra intro preview";
  }
  if (introVideoSummary) {
    introVideoSummary.textContent = selectedVideo.summary || "A calm, branded introduction that leads cleanly into the studio.";
  }
  if (introVideoTag) {
    introVideoTag.textContent = mode === "signup" ? "New user intro" : "Welcome back";
  }
  if (introVideoToggle) {
    introVideoToggle.disabled = false;
    introVideoToggle.textContent = introVideoPlayer.paused ? "Play" : "Pause";
  }
}

async function toggleIntroVideoPlayback() {
  if (!introVideoPlayer || introVideoPlayer.disabled) {
    return;
  }
  if (introVideoPlayer.paused) {
    try {
      await introVideoPlayer.play();
    } catch (error) {
      console.warn("Could not play intro video:", error);
      return;
    }
    if (introVideoToggle) {
      introVideoToggle.textContent = "Pause";
    }
    if (introSoundBtn) {
      introSoundBtn.textContent = "Mute sound";
    }
    return;
  }
  introVideoPlayer.pause();
  if (introVideoToggle) {
    introVideoToggle.textContent = "Play";
  }
  if (introSoundBtn) {
    introSoundBtn.textContent = "Play with sound";
  }
}

async function toggleIntroVideoSound() {
  if (!introVideoPlayer) {
    return;
  }
  introVideoPlayer.muted = !introVideoPlayer.muted;
  if (!introVideoPlayer.paused) {
    try {
      await introVideoPlayer.play();
    } catch (error) {
      console.warn("Could not adjust intro sound:", error);
    }
  }
  if (introSoundBtn) {
    introSoundBtn.textContent = introVideoPlayer.muted ? "Play with sound" : "Mute sound";
  }
}

function openIntroScreen(profile, mode = "signin") {
  introVideoMode = mode;
  if (introScreen) {
    introScreen.classList.remove("hidden");
  }
  if (loginScreen) {
    loginScreen.classList.add("hidden");
  }
  if (appShell) {
    appShell.classList.add("hidden");
  }
  if (introTitle) {
    introTitle.textContent = mode === "signup"
      ? `Welcome to Astra, ${profile && profile.name ? profile.name : "student"}`
      : `Welcome back to Astra, ${profile && profile.name ? profile.name : "student"}`;
  }
  if (introQuote) {
    introQuote.textContent = mode === "signup"
      ? "A clean welcome, then a smooth move into your learning studio."
      : "A short reset, then right back into your learning rhythm.";
  }
  if (introText) {
    introText.textContent = mode === "signup"
      ? "This introduction is designed to feel calm, premium, and intentional. The video helps set the tone, then the studio opens without breaking the flow."
      : "Astra keeps the transition soft and focused so your return feels natural. You get a quick welcome, a branded video moment, and then the learning studio opens.";
  }
  if (introHint) {
    introHint.textContent = "When you're ready, continue into the studio and keep moving.";
  }
  renderIntroVideo(videoLibrarySnapshot || authHeroVideoSnapshot, mode);
  if (introVideoPlayer) {
    try {
      introVideoPlayer.currentTime = 0;
    } catch (error) {
      void error;
    }
  }
}

function enterStudioFromIntro() {
  if (introVideoPlayer) {
    introVideoPlayer.pause();
    introVideoPlayer.muted = true;
  }
  if (introVideoToggle) {
    introVideoToggle.textContent = "Play";
  }
  if (introSoundBtn) {
    introSoundBtn.textContent = "Play with sound";
  }
  if (introScreen) {
    introScreen.classList.add("hidden");
  }
  if (appShell) {
    appShell.classList.remove("hidden");
  }
  setActiveTab("tutorTab");
}

async function fetchVideoLibrary(studentName = "") {
  const suffix = studentName ? `?student_name=${encodeURIComponent(studentName)}` : "";
  const response = await fetch(`/api/video-library${suffix}`);
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || "Could not load the video library.");
  }
  renderAuthHeroVideo(payload);
  renderVideoLibrary(payload);
  if (introScreen && !introScreen.classList.contains("hidden")) {
    renderIntroVideo(payload, introVideoMode);
  }
}

function openActiveTutorVideoBridge() {
  if (!activeTutorVideo) {
    return;
  }
  renderVisualLearning(activeTutorVideo.visual_learning || null);
  renderVideoExplanation(activeTutorVideo.video_explanation || null);
  renderReasoningPanel(activeTutorVideo.video_explanation || null);
  renderSummaryPanel(activeTutorVideo.summary || "");
  ensureTutorRoomPersona();
  if (document.querySelector('.tab-panel.active')?.id !== "videoTutorTab") {
    setActiveTab("videoTutorTab");
  }
  setActiveStudioPane("threeTutorPanel");
}

function useActiveTutorVideoInTutor() {
  if (!activeTutorVideo) {
    return;
  }
  const promptSeed = activeTutorVideo.topic || activeTutorVideo.title || "this concept";
  const targetInput = messageInput;
  if (targetInput) {
    targetInput.value = `Teach me ${promptSeed} using the same style as the selected tutor video and then connect it to a 3D visual explanation.`;
  }
  setActiveTab("tutorTab");
  if (targetInput) {
    targetInput.focus();
  }
}

async function fetchLearningSources(studentName) {
  if (!studentName) {
    renderLearningSources([]);
    renderLearningSourcePack(null, "");
    return;
  }
  const response = await fetch(`/api/learning-sources/${encodeURIComponent(studentName)}`);
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || "Could not load learning sources.");
  }
  renderLearningSourcePack(payload.source_pack || null, payload.student_state_route_text || "");
  renderLearningSources(payload.resources || []);
}

function renderSyllabusDocuments(documents) {
  if (!syllabusManager) {
    return;
  }
  syllabusManager.innerHTML = "";
  if (!documents || !documents.length) {
    syllabusManager.innerHTML = `<p class="muted">No syllabus documents saved yet. Add a course portion to help the tutor prepare around your actual topics.</p>`;
    return;
  }

  documents.forEach((documentItem) => {
    const card = document.createElement("div");
    card.className = "exam-card";
    const title = document.createElement("strong");
    title.textContent = documentItem.title || "Syllabus";
    const meta = document.createElement("p");
    meta.className = "muted";
    meta.textContent = `${documentItem.source_type === "document" ? "Uploaded file" : "Pasted text"}${documentItem.file_name ? ` | ${documentItem.file_name}` : ""}`;
    const summary = document.createElement("p");
    summary.className = "muted";
    summary.textContent = documentItem.topic_summary || "No summary available yet.";
    const removeBtn = document.createElement("button");
    removeBtn.type = "button";
    removeBtn.className = "ghost-button";
    removeBtn.textContent = "Delete";
    removeBtn.addEventListener("click", () => deleteSyllabusDocument(documentItem.id));
    card.append(title, meta, summary, removeBtn);
    syllabusManager.appendChild(card);
  });
}

async function fetchSyllabusDocuments(studentName) {
  if (!studentName) {
    renderSyllabusDocuments([]);
    return;
  }
  const response = await fetch(`/api/syllabus/${encodeURIComponent(studentName)}`);
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || "Could not load syllabus documents.");
  }
  renderSyllabusDocuments(payload.documents || []);
}

async function deleteSyllabusDocument(documentId) {
  if (!activeProfile) {
    return;
  }
  const response = await fetch("/api/syllabus/delete", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      student_name: activeProfile.name,
      document_id: documentId,
    }),
  });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || "Could not delete that syllabus document.");
  }
  renderSyllabusDocuments(payload.documents || []);
  renderStorageStatus(payload.storage_status || null);
  if (syllabusStatus) {
    syllabusStatus.textContent = "The selected syllabus document was deleted.";
  }
}

function readLocalFileAsBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const result = String(reader.result || "");
      const base64 = result.includes(",") ? result.split(",")[1] : result;
      resolve(base64);
    };
    reader.onerror = () => reject(new Error("Could not read that file."));
    reader.readAsDataURL(file);
  });
}

async function uploadSyllabusMaterial() {
  if (!activeProfile) {
    return;
  }

  const title = (syllabusTitleInput && syllabusTitleInput.value.trim()) || "";
  const textContent = (syllabusTextInput && syllabusTextInput.value.trim()) || "";
  const file = syllabusFileInput && syllabusFileInput.files && syllabusFileInput.files[0];

  if (!textContent && !file) {
    if (syllabusStatus) {
      syllabusStatus.textContent = "Paste some syllabus text or choose a file first.";
    }
    return;
  }

  let fileBase64 = "";
  let fileName = "";
  let mimeType = "";
  if (file) {
    fileBase64 = await readLocalFileAsBase64(file);
    fileName = file.name || "";
    mimeType = file.type || "";
  }

  if (uploadSyllabusBtn) {
    uploadSyllabusBtn.disabled = true;
  }
  if (syllabusStatus) {
    syllabusStatus.textContent = "Saving and analyzing your syllabus...";
  }

  try {
    const response = await fetch("/api/syllabus/upload", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        student_name: activeProfile.name,
        title,
        text_content: textContent,
        file_base64: fileBase64,
        file_name: fileName,
        mime_type: mimeType,
      }),
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Could not save that syllabus.");
    }
    renderSyllabusDocuments(payload.documents || []);
    renderStorageStatus(payload.storage_status || null);
    if (syllabusTitleInput) {
      syllabusTitleInput.value = "";
    }
    if (syllabusTextInput) {
      syllabusTextInput.value = "";
    }
    if (syllabusFileInput) {
      syllabusFileInput.value = "";
    }
    if (syllabusStatus) {
      syllabusStatus.textContent = "Syllabus saved. The tutor and revision planner will use it from now on.";
    }
  } catch (error) {
    if (syllabusStatus) {
      syllabusStatus.textContent = error.message;
    }
  } finally {
    if (uploadSyllabusBtn) {
      uploadSyllabusBtn.disabled = false;
    }
  }
}

function appendMessage(mode, role, text) {
  const feed = getFeedForMode(mode);
  if (!feed) {
    return null;
  }
  const paragraph = appendFeedMessage(feed, mode, role, text);
  if (mode === "tutor" && tutorRoomTranscriptFeed) {
    appendFeedMessage(tutorRoomTranscriptFeed, mode, role, text);
  }
  syncTutorFullscreenOverlay();
  syncLoungeFullscreenOverlay();
  return paragraph;
}

function clearTutorCheckpointWidget() {
  const feed = getFeedForMode("tutor");
  if (!feed) {
    return;
  }
  const existing = feed.querySelector(".checkpoint-card");
  if (existing) {
    existing.remove();
  }
  const existingPractice = feed.querySelector(".checkpoint-practice-stack");
  if (existingPractice) {
    existingPractice.remove();
  }
  if (tutorRoomTranscriptFeed) {
    const transcriptExisting = tutorRoomTranscriptFeed.querySelector(".checkpoint-card");
    if (transcriptExisting) {
      transcriptExisting.remove();
    }
    const transcriptPractice = tutorRoomTranscriptFeed.querySelector(".checkpoint-practice-stack");
    if (transcriptPractice) {
      transcriptPractice.remove();
    }
  }
  syncTutorFullscreenOverlay();
  activeTutorCheckpoint = null;
}

function _checkpointOptionLabel(index) {
  return String.fromCharCode(65 + index);
}

function renderTutorCheckpointWidget(checkpoint, { practiceMode = false } = {}) {
  const feed = getFeedForMode("tutor");
  if (!feed || !checkpoint) {
    return null;
  }

  const card = document.createElement("div");
  card.className = `checkpoint-card${practiceMode ? " practice-mode" : ""}`;
  card.dataset.checkpointMode = practiceMode ? "practice" : "checkpoint";

  const header = document.createElement("div");
  header.className = "checkpoint-header";
  const headingCopy = document.createElement("div");
  const heading = document.createElement("p");
  heading.className = "card-title";
  heading.textContent = checkpoint.heading || (practiceMode ? "More practice" : "Quick Check - let's see if this clicked");
  const meta = document.createElement("p");
  meta.className = "muted checkpoint-meta";
  const metaBits = [];
  if (checkpoint.subject) {
    metaBits.push(checkpoint.subject);
  }
  if (checkpoint.difficulty) {
    metaBits.push(checkpoint.difficulty);
  }
  if (checkpoint.explanation_level) {
    metaBits.push(`Level ${checkpoint.explanation_level}`);
  }
  meta.textContent = metaBits.length ? metaBits.join(" - ") : "JEE checkpoint";
  headingCopy.append(heading, meta);
  const badge = document.createElement("span");
  badge.className = "pill";
  badge.textContent = practiceMode ? "Practice" : "Checkpoint";
  header.append(headingCopy, badge);

  const question = document.createElement("p");
  question.className = "checkpoint-question";
  question.textContent = checkpoint.question || "Question unavailable.";

  const options = document.createElement("div");
  options.className = "checkpoint-options";

  const result = document.createElement("div");
  result.className = "checkpoint-result hidden";

  const supportRow = document.createElement("div");
  supportRow.className = "checkpoint-support-row";
  const morePracticeBtn = document.createElement("button");
  morePracticeBtn.type = "button";
  morePracticeBtn.className = "ghost-button hidden";
  morePracticeBtn.textContent = "More practice";
  supportRow.appendChild(morePracticeBtn);

  const optionButtons = [];
  const lockOptions = () => {
    optionButtons.forEach((button) => {
      button.disabled = true;
    });
  };

  const showResult = (evaluation, selectedAnswer) => {
    result.classList.remove("hidden");
    result.innerHTML = "";
    const resultHeading = document.createElement("strong");
    resultHeading.textContent = evaluation.is_correct ? "Correct" : "Let's fix that together";
    const feedback = document.createElement("p");
    feedback.className = "muted";
    feedback.textContent = evaluation.feedback || (evaluation.is_correct ? "Nice work - that clicked." : "That needs one more pass.");
    result.append(resultHeading, feedback);

    if (evaluation.is_correct) {
      const practiceHint = document.createElement("p");
      practiceHint.className = "muted";
      practiceHint.textContent = evaluation.more_practice_heading || "You can open three extra questions on the same topic if you want a stronger grip.";
      result.appendChild(practiceHint);
      morePracticeBtn.classList.remove("hidden");
      morePracticeBtn.disabled = false;
      morePracticeBtn.onclick = async () => {
        morePracticeBtn.disabled = true;
        morePracticeBtn.textContent = "Loading...";
        try {
          const practice = await fetchCheckpointSet({
            topic: checkpoint.topic,
            subject: checkpoint.subject,
            explanation_level: checkpoint.explanation_level,
            original_explanation: checkpoint.original_explanation || checkpoint.correct_explanation || checkpoint.question,
            practice_count: 3,
          });
          renderCheckpointPracticeSet(practice.practice_questions || [], card);
          morePracticeBtn.classList.add("hidden");
        } catch (error) {
          result.appendChild(createMutedLine(`Could not load more practice: ${error.message}`));
          morePracticeBtn.disabled = false;
          morePracticeBtn.textContent = "More practice";
        }
      };
    } else {
      const wrongReason = document.createElement("p");
      wrongReason.className = "checkpoint-detail";
      wrongReason.textContent = evaluation.wrong_reason || "That choice misses the exact rule from the explanation.";
      const reExplain = document.createElement("p");
      reExplain.className = "checkpoint-detail";
      reExplain.textContent = evaluation.re_explanation || "Try the same concept through a different example.";
      const correctAnswer = document.createElement("p");
      correctAnswer.className = "checkpoint-detail";
      correctAnswer.textContent = `Correct answer: ${evaluation.correct_answer || checkpoint.correct_answer} - ${evaluation.correct_explanation || checkpoint.correct_explanation || ""}`;
      result.append(wrongReason, reExplain, correctAnswer);
      morePracticeBtn.classList.add("hidden");
    }
  };

  const handleSelection = async (optionLabel, optionText) => {
    lockOptions();
    result.classList.remove("hidden");
    result.innerHTML = "";
    result.appendChild(createMutedLine("Checking your answer..."));
    try {
      const evaluation = await evaluateCheckpointAnswer({
        question: checkpoint.question,
        correct_answer: checkpoint.correct_answer,
        student_answer: optionLabel,
        topic: checkpoint.topic,
        subject: checkpoint.subject,
        explanation_level: checkpoint.explanation_level,
        original_explanation: checkpoint.original_explanation || checkpoint.correct_explanation || checkpoint.question,
      });
      showResult(evaluation, optionText);
      updateSessionCheckpointStats({
        topic: checkpoint.topic || checkpoint.question || "Checkpoint",
        score: evaluation.is_correct ? 100 : 45,
        confidence: evaluation.is_correct ? "good" : "medium",
      });
      logSessionActivity(`Checkpoint answered for ${checkpoint.topic || "this topic"}: ${evaluation.is_correct ? "correct" : "needs revision"}`);
      setAstraStatus(
        evaluation.is_correct
          ? `Updating your progress... ${checkpoint.topic || "this topic"} confidence: good`
          : `Updating your progress... ${checkpoint.topic || "this topic"} confidence: medium`,
        "working",
        true
      );
      if (!practiceMode && activeJourneySession) {
        const checkpointScore = evaluation.is_correct ? 100 : 45;
        await completeJourneySessionFromCheckpoint(checkpointScore);
      }
    } catch (error) {
      result.innerHTML = "";
      result.appendChild(createMutedLine(`Could not check that answer: ${error.message}`));
    }
    syncTutorRoomTranscript();
  };

  (checkpoint.options || []).slice(0, 4).forEach((option, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "mock-option checkpoint-option";
    button.textContent = `${_checkpointOptionLabel(index)}. ${option}`;
    button.addEventListener("click", () => handleSelection(_checkpointOptionLabel(index), option));
    optionButtons.push(button);
    options.appendChild(button);
  });

  card.append(header, question, options, result, supportRow);
  feed.appendChild(card);
  feed.scrollTop = feed.scrollHeight;
  syncTutorFullscreenOverlay();
  syncTutorRoomTranscript();
  return card;
}

function renderTutorPracticeSet(practiceQuestions, anchorCard, options = {}) {
  const feed = getFeedForMode("tutor");
  if (!feed || !Array.isArray(practiceQuestions) || !practiceQuestions.length) {
    return;
  }

  const existingPractice = feed.querySelector(".checkpoint-practice-stack");
  if (existingPractice) {
    existingPractice.remove();
  }

  const container = document.createElement("div");
  container.className = "checkpoint-practice-stack";
  const answerStates = new Array(practiceQuestions.length).fill(null);
  let completionStarted = false;

  const maybeCompleteChapterCheckpoint = async () => {
    if (!options.chapterMode || completionStarted) {
      return;
    }
    if (answerStates.some((item) => item === null)) {
      return;
    }
    completionStarted = true;
    const correctCount = answerStates.filter(Boolean).length;
    const totalCount = answerStates.length || 1;
    const checkpointScore = Math.round((correctCount * 100) / totalCount);
    const summary = document.createElement("div");
    summary.className = "checkpoint-result";
    summary.innerHTML = "";
    summary.appendChild(createMutedLine(`Subtopic checkpoint score: ${checkpointScore}% (${correctCount}/${totalCount})`));
    container.appendChild(summary);
    if (typeof options.onComplete === "function") {
      await options.onComplete({ correctCount, totalCount, checkpointScore, answers: answerStates.slice() });
    }
  };

  practiceQuestions.slice(0, 3).forEach((question, index) => {
    const card = document.createElement("div");
    card.className = "checkpoint-card practice-mode";
    const header = document.createElement("div");
    header.className = "checkpoint-header";
    const headingCopy = document.createElement("div");
    const heading = document.createElement("p");
    heading.className = "card-title";
    heading.textContent = question.heading || `More practice ${index + 1}`;
    const meta = document.createElement("p");
    meta.className = "muted checkpoint-meta";
    const metaBits = [];
    if (question.subject) {
      metaBits.push(question.subject);
    }
    if (question.difficulty) {
      metaBits.push(question.difficulty);
    }
    meta.textContent = metaBits.length ? metaBits.join(" - ") : "Practice question";
    headingCopy.append(heading, meta);
    const badge = document.createElement("span");
    badge.className = "pill";
    badge.textContent = `Practice ${index + 1}`;
    header.append(headingCopy, badge);

    const prompt = document.createElement("p");
    prompt.className = "checkpoint-question";
    renderMarkdownElement(prompt, question.question || "Question unavailable.");

    const options = document.createElement("div");
    options.className = "checkpoint-options";
    const result = document.createElement("div");
    result.className = "checkpoint-result hidden";
    const optionButtons = [];
    const lockOptions = () => optionButtons.forEach((button) => { button.disabled = true; });

    const showResult = (evaluation) => {
      result.classList.remove("hidden");
      result.innerHTML = "";
      const feedback = document.createElement("strong");
      feedback.textContent = evaluation.is_correct ? "Correct" : "Review this one";
      const detail = document.createElement("p");
      detail.className = "muted";
      detail.textContent = evaluation.feedback || (evaluation.is_correct ? "Nice work." : "Let's use the explanation to tighten the idea.");
      const explanation = document.createElement("p");
      explanation.className = "checkpoint-detail";
      explanation.textContent = evaluation.correct_explanation || question.correct_explanation || "";
      result.append(feedback, detail, explanation);
      if (!evaluation.is_correct && evaluation.wrong_reason) {
        const wrong = document.createElement("p");
        wrong.className = "checkpoint-detail";
        wrong.textContent = evaluation.wrong_reason;
        result.appendChild(wrong);
      }
      answerStates[index] = Boolean(evaluation.is_correct);
      void maybeCompleteChapterCheckpoint();
    };

    const handleSelection = async (optionLabel) => {
      lockOptions();
      result.classList.remove("hidden");
      result.innerHTML = "";
      result.appendChild(createMutedLine("Checking your answer..."));
      try {
        const evaluation = await evaluateCheckpointAnswer({
          question: question.question,
          correct_answer: question.correct_answer,
          student_answer: optionLabel,
          topic: question.topic,
          subject: question.subject,
          explanation_level: question.explanation_level,
          original_explanation: question.correct_explanation || question.question,
        });
        showResult(evaluation);
      } catch (error) {
        result.innerHTML = "";
        result.appendChild(createMutedLine(`Could not check that answer: ${error.message}`));
      }
      syncTutorRoomTranscript();
    };

    (question.options || []).slice(0, 4).forEach((option, optionIndex) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "mock-option checkpoint-option";
      button.textContent = `${_checkpointOptionLabel(optionIndex)}. ${option}`;
      button.addEventListener("click", () => handleSelection(_checkpointOptionLabel(optionIndex)));
      optionButtons.push(button);
      options.appendChild(button);
    });

    card.append(header, prompt, options, result);
    container.appendChild(card);
  });

  if (anchorCard && anchorCard.parentElement === feed) {
    anchorCard.insertAdjacentElement("afterend", container);
  } else {
    feed.appendChild(container);
  }
  feed.scrollTop = feed.scrollHeight;
  syncTutorFullscreenOverlay();
  syncTutorRoomTranscript();
}

async function fetchCheckpointSet(payload) {
  console.log("CHECKPOINT TRIGGERED - fetching question");
  const response = await fetch("/api/checkpoint/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await response.json();
  console.log("CHECKPOINT RESPONSE:", data);
  if (!response.ok) {
    throw new Error(data.detail || "Could not build a checkpoint.");
  }
  return data;
}

async function loadTutorCheckpoint(topic, subject, explanationLevel, originalExplanation, options = {}) {
  if (!activeProfile) {
    return;
  }
  const topicLabel = String(topic || "").trim() || "this topic";
  const subjectLabel = String(subject || "").trim() || "your subject";
  try {
    clearTutorCheckpointWidget();
    const chapterMode = Boolean(options.chapterMode) || isChapterCheckpointActive();
    const practiceCount = chapterMode ? 3 : Number(options.practiceCount || 0);
    setAstraStatus(
      chapterMode
        ? "Pulling from JEE PYQ database..."
        : `Searching NCERT ${subjectLabel} sources...`,
      "working"
    );
    showKnowledgeBaseTag(
      chapterMode
        ? "Pulling from JEE PYQ database..."
        : `Pulling from NCERT ${subjectLabel} sources...`,
      true
    );
    const chapterCheckpointStartedAt = Date.now();
    const checkpoint = await fetchCheckpointSet({
      student_name: activeProfile.name,
      topic,
      subject,
      explanation_level: explanationLevel,
      original_explanation: originalExplanation,
      practice_count: practiceCount,
    });
    activeTutorCheckpoint = checkpoint;
    if (sessionCheckpointStats.topic !== topicLabel) {
      sessionCheckpointStats = {
        answered: 0,
        average: 0,
        confidence: "new",
        topic: topicLabel,
      };
    }
    renderSessionStats(topicLabel, sessionCheckpointStats.confidence || "new", sessionCheckpointStats.average || 0);
    logSessionActivity(`Loaded checkpoint for ${topicLabel}`);
    if (chapterMode && Array.isArray(checkpoint.practice_questions) && checkpoint.practice_questions.length) {
      renderTutorPracticeSet(checkpoint.practice_questions, null, {
        chapterMode: true,
        onComplete: async ({ correctCount, totalCount }) => {
          const score = totalCount ? Math.round((Number(correctCount || 0) * 100) / totalCount) : 0;
          const elapsedMinutes = Math.max(1, Math.round((Date.now() - chapterCheckpointStartedAt) / 60000));
          updateSessionCheckpointStats({ topic: topicLabel, score, confidence: score >= 85 ? "strong" : score >= 70 ? "good" : score >= 50 ? "medium" : "low" });
          logSessionActivity(`Checkpoint ${Math.min(sessionCheckpointStats.answered, 99)} on ${topicLabel}: ${score}/100`);
          await completeChapterSubtopicFromCheckpoint(score, elapsedMinutes);
        },
      });
    } else {
      renderTutorCheckpointWidget(checkpoint);
    }
    showKnowledgeBaseTag("", false);
    setAstraStatus(`Astra is ready. Today's focus: ${topicLabel} - ${subjectLabel}`, "idle");
    return checkpoint;
  } catch (error) {
    console.warn("Checkpoint generation skipped:", error);
    showKnowledgeBaseTag("", false);
    setAstraStatus(`Checkpoint ready. ${topicLabel}`, "idle");
    return null;
  }
}

async function evaluateCheckpointAnswer(payload) {
  const response = await fetch("/api/checkpoint/evaluate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Could not evaluate that checkpoint.");
  }
  return data;
}

function createMutedLine(text) {
  const paragraph = document.createElement("p");
  paragraph.className = "muted";
  paragraph.textContent = text;
  return paragraph;
}

function escapeHtml(text) {
  return String(text || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function normalizeTutorMathText(text) {
  let source = String(text || "");
  if (!source) {
    return "";
  }
  source = source.replace(/\\frac\{\\text\{d\}\}\{\\text\{dt\}\}/g, "d/dt");
  source = source.replace(/\\frac\{d\}\{dt\}/g, "d/dt");
  source = source.replace(/\\frac\{([^{}\n]+)\}\{([^{}\n]+)\}/g, "($1)/($2)");
  source = source.replace(/\\text\{([^{}]*)\}/g, "$1");
  source = source.replace(/\\sqrt\{([^{}]*)\}/g, "âˆš($1)");
  source = source.replace(/\\left|\\right/g, "");
  source = source.replace(/\\times/g, " Ã— ");
  source = source.replace(/\\cdot/g, " Â· ");
  source = source.replace(/\\pi/g, "Ï€");
  source = source.replace(/\\theta/g, "Î¸");
  source = source.replace(/\\alpha/g, "Î±");
  source = source.replace(/\\beta/g, "Î²");
  source = source.replace(/\\gamma/g, "Î³");
  source = source.replace(/\\omega/g, "Ï‰");
  source = source.replace(/\\Delta/g, "Î”");
  source = source.replace(/\\lambda/g, "Î»");
  source = source.replace(/\\mu/g, "Î¼");
  source = source.replace(/\\[a-zA-Z]+/g, "");
  source = source.replace(/\$/g, "");
  source = source.replace(/[{}]/g, "");
  source = source.replace(/\btheta\b/g, "Î¸");
  source = source.replace(/\balpha\b/g, "Î±");
  source = source.replace(/\bbeta\b/g, "Î²");
  source = source.replace(/\bgamma\b/g, "Î³");
  source = source.replace(/\bomega\b/g, "Ï‰");
  source = source.replace(/\bpi\b/g, "Ï€");
  source = source.replace(/\blambda\b/g, "Î»");
  source = source.replace(/\bmu\b/g, "Î¼");
  source = source.replace(/\bDelta\b/g, "Î”");
  source = source.replace(/sqrt\(([^()]+)\)/g, "âˆš($1)");
  source = source.replace(/\^2\b/g, "Â²");
  source = source.replace(/\^3\b/g, "Â³");
  source = source.replace(/\^\(([^)]+)\)/g, "^$1");
  source = source.replace(/([A-Za-z0-9)Â²Â³])\s*\*\s*([A-Za-z0-9(Î¸Ï€Î±Î²Î³Î»Ï‰Î¼âˆš])/g, "$1 Â· $2");
  source = source.replace(/[ \t]{2,}/g, " ");
  return source;
}

function normalizeFormulaSubject(value) {
  const normalized = String(value || "").trim().toLowerCase();
  if (normalized === "math" || normalized === "maths") {
    return "mathematics";
  }
  return normalized || "physics";
}

function formulaSubjectLabel(subject) {
  const normalized = normalizeFormulaSubject(subject);
  if (normalized === "mathematics") {
    return "Maths";
  }
  return normalized.charAt(0).toUpperCase() + normalized.slice(1);
}

function formulaChapterKey(chapter) {
  return `${normalizeFormulaSubject(chapter.subject)}:${chapter.id}`;
}

function normalizeFormulaTerm(value) {
  return String(value || "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, " ")
    .trim();
}

function formulaMatchesWeak(chapter) {
  if (!formulaWeakTopicTerms.size) {
    return false;
  }
  const chapterTerms = [
    normalizeFormulaTerm(chapter.id),
    normalizeFormulaTerm(chapter.name),
    normalizeFormulaTerm(chapter.subject),
  ].filter(Boolean);
  return chapterTerms.some((term) => {
    if (formulaWeakTopicTerms.has(term)) {
      return true;
    }
    return Array.from(formulaWeakTopicTerms).some((weakTerm) => term.includes(weakTerm) || weakTerm.includes(term));
  });
}

function flattenFormulaDatabase(database) {
  const subjects = database && database.subjects ? database.subjects : {};
  return Object.entries(subjects).flatMap(([subject, payload]) => {
    const chapters = Array.isArray(payload && payload.chapters) ? payload.chapters : [];
    return chapters.map((chapter) => ({
      ...chapter,
      subject: normalizeFormulaSubject(subject),
    }));
  });
}

function highlightFormulaMatch(text, query) {
  const source = escapeHtml(text);
  const needle = String(query || "").trim();
  if (!needle) {
    return source;
  }
  const escapedNeedle = needle.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return source.replace(new RegExp(`(${escapedNeedle})`, "ig"), '<mark class="formula-highlight">$1</mark>');
}

function getFormulaSearchBlob(chapter, formula) {
  const variables = formula && typeof formula.variables === "object" && formula.variables ? formula.variables : {};
  return [
    chapter.subject,
    chapter.name,
    chapter.id,
    formula.id,
    formula.name,
    formula.formula,
    formula.condition,
    formula.jee_tip,
    formula.quick_memory,
    Object.keys(variables).join(" "),
    Object.values(variables).join(" "),
  ].join(" ").toLowerCase();
}

function setFormulasStatus(message) {
  if (formulasStatus) {
    formulasStatus.textContent = message || "";
    formulasStatus.classList.toggle("hidden", !message);
  }
}

function setFormulaChapterDropdown(open) {
  if (!formulasChapterDropdownPanel || !formulasChapterToggle) {
    return;
  }
  formulasChapterDropdownPanel.classList.toggle("hidden", !open);
  formulasChapterToggle.setAttribute("aria-expanded", String(open));
}

function closeFormulaChapterDropdown() {
  setFormulaChapterDropdown(false);
}

async function loadFormulaDatabase(force = false) {
  if (!formulasChapterList || (!force && formulasDatabase)) {
    if (formulasDatabase) {
      renderFormulaChapterList();
      renderFormulaDetail();
    }
    return;
  }
  try {
    setFormulasStatus("Loading formulas...");
    const response = await fetch("/api/formulas/all");
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Could not load formulas.");
    }
    formulasDatabase = payload;
    formulaChapters = flattenFormulaDatabase(payload);
    if (!selectedFormulaChapterKey && formulaChapters.length) {
      selectedFormulaChapterKey = formulaChapterKey(formulaChapters[0]);
    }
    setFormulasStatus("");
    renderFormulaChapterList();
    renderFormulaDetail();
  } catch (error) {
    console.warn("Could not load formulas:", error);
    setFormulasStatus(`Could not load formulas: ${error.message}`);
  }
}

function getVisibleFormulaChapters() {
  const visible = formulaChapters.filter((chapter) => activeFormulaSubjects.has(normalizeFormulaSubject(chapter.subject)));
  if (!formulasWeakToggle || !formulasWeakToggle.checked) {
    return visible;
  }
  return [...visible].sort((first, second) => {
    const firstWeak = formulaMatchesWeak(first) ? 0 : 1;
    const secondWeak = formulaMatchesWeak(second) ? 0 : 1;
    if (firstWeak !== secondWeak) {
      return firstWeak - secondWeak;
    }
    return (first.unit_number || 0) - (second.unit_number || 0);
  });
}

function renderFormulaChapterList() {
  if (!formulasChapterList) {
    return;
  }
  const chapters = getVisibleFormulaChapters();
  if (!chapters.length) {
    formulasChapterList.innerHTML = '<p class="muted">No chapters match the selected subjects.</p>';
    return;
  }
  if (!chapters.some((chapter) => formulaChapterKey(chapter) === selectedFormulaChapterKey)) {
    selectedFormulaChapterKey = formulaChapterKey(chapters[0]);
  }
  const selectedChapter = chapters.find((chapter) => formulaChapterKey(chapter) === selectedFormulaChapterKey);
  if (formulasChapterToggleText) {
    formulasChapterToggleText.textContent = selectedChapter
      ? `${formulaSubjectLabel(selectedChapter.subject)} - ${selectedChapter.name}`
      : "Choose chapter";
  }
  formulasChapterList.innerHTML = chapters.map((chapter) => {
    const key = formulaChapterKey(chapter);
    const subject = normalizeFormulaSubject(chapter.subject);
    const formulaCount = Array.isArray(chapter.formulas) ? chapter.formulas.length : 0;
    const focusBadge = formulaMatchesWeak(chapter) ? '<span class="pill">Focus Here</span>' : "";
    return `
      <button type="button" class="formula-chapter-button ${key === selectedFormulaChapterKey ? "active" : ""}" data-formula-chapter="${escapeHtml(key)}">
        <div class="formula-chapter-title-row">
          <span><span class="formula-subject-dot ${escapeHtml(subject)}"></span> <strong>${escapeHtml(chapter.name)}</strong></span>
          ${focusBadge}
        </div>
        <div class="formula-card-meta">
          <span class="pill">${escapeHtml(formulaSubjectLabel(subject))}</span>
          <span class="pill">${formulaCount} formulas</span>
          <span class="pill">${escapeHtml(String(chapter.jee_weightage || 0))}% weightage</span>
        </div>
      </button>
    `;
  }).join("");
  formulasChapterList.querySelectorAll("[data-formula-chapter]").forEach((button) => {
    button.addEventListener("click", () => {
      selectedFormulaChapterKey = button.dataset.formulaChapter || "";
      if (formulasSearchInput) {
        formulasSearchInput.value = "";
      }
      renderFormulaChapterList();
      renderFormulaDetail();
      closeFormulaChapterDropdown();
    });
  });
}

function renderFormulaCard(formula, query = "") {
  const variables = formula && typeof formula.variables === "object" && formula.variables ? formula.variables : {};
  const variableChips = Object.entries(variables).map(([key, value]) => (
    `<span class="pill"><strong>${highlightFormulaMatch(key, query)}</strong>: ${highlightFormulaMatch(value, query)}</span>`
  )).join("");
  return `
    <article class="formula-card">
      <p class="card-title">${highlightFormulaMatch(formula.name || "Formula", query)}</p>
      <div class="formula-display-text">${highlightFormulaMatch(formula.formula || "-", query)}</div>
      <div class="formula-chip-row">${variableChips}</div>
      ${formula.condition ? `<p class="muted">Condition: ${highlightFormulaMatch(formula.condition, query)}</p>` : ""}
      ${formula.jee_tip ? `<div class="formula-tip-box"><strong>JEE Tip:</strong> ${highlightFormulaMatch(formula.jee_tip, query)}</div>` : ""}
      ${formula.quick_memory ? `<p class="muted"><strong>Quick memory:</strong> ${highlightFormulaMatch(formula.quick_memory, query)}</p>` : ""}
    </article>
  `;
}

function renderFormulaChapterDetail(chapter, query = "") {
  if (!chapter) {
    return;
  }
  if (formulasChapterSubject) {
    formulasChapterSubject.textContent = formulaSubjectLabel(chapter.subject);
  }
  if (formulasChapterTitle) {
    formulasChapterTitle.textContent = chapter.name || "Formula sheet";
  }
  if (formulasWeightageChip) {
    formulasWeightageChip.textContent = `${chapter.jee_weightage || 0}% weightage`;
  }
  const formulas = Array.isArray(chapter.formulas) ? chapter.formulas : [];
  const shortcuts = Array.isArray(chapter.shortcuts) ? chapter.shortcuts : [];
  const mistakes = Array.isArray(chapter.common_mistakes) ? chapter.common_mistakes : [];
  if (formulasFormulaList) {
    formulasFormulaList.innerHTML = formulas.length
      ? formulas.map((formula) => renderFormulaCard(formula, query)).join("")
      : '<p class="muted">No formulas found for this chapter yet.</p>';
  }
  if (formulasShortcutList) {
    formulasShortcutList.innerHTML = shortcuts.length
      ? shortcuts.map((shortcut) => `
        <article class="formula-shortcut-card">
          <p class="card-title">${highlightFormulaMatch(shortcut.title || "Shortcut", query)}</p>
          <p class="muted">${highlightFormulaMatch(shortcut.detail || "", query)}</p>
        </article>
      `).join("")
      : '<p class="muted">No shortcuts listed for this chapter yet.</p>';
  }
  if (formulasMistakeList) {
    formulasMistakeList.innerHTML = mistakes.length
      ? mistakes.map((mistake) => `<li>${highlightFormulaMatch(mistake, query)}</li>`).join("")
      : '<li>No common mistakes listed yet.</li>';
  }
}

function renderFormulaSearchResults(query) {
  const normalizedQuery = String(query || "").trim().toLowerCase();
  const chapters = getVisibleFormulaChapters();
  const groups = chapters.map((chapter) => {
    const formulas = (chapter.formulas || []).filter((formula) => getFormulaSearchBlob(chapter, formula).includes(normalizedQuery));
    const shortcuts = (chapter.shortcuts || []).filter((shortcut) => (
      `${shortcut.title || ""} ${shortcut.detail || ""} ${chapter.name || ""}`.toLowerCase().includes(normalizedQuery)
    ));
    return { chapter, formulas, shortcuts };
  }).filter((group) => group.formulas.length || group.shortcuts.length);
  if (formulasChapterSubject) {
    formulasChapterSubject.textContent = "Search Results";
  }
  if (formulasChapterTitle) {
    formulasChapterTitle.textContent = `Matches for "${query}"`;
  }
  if (formulasWeightageChip) {
    formulasWeightageChip.textContent = `${groups.length} chapters`;
  }
  if (!groups.length) {
    if (formulasFormulaList) {
      formulasFormulaList.innerHTML = '<p class="muted">No formulas match that search.</p>';
    }
    if (formulasShortcutList) {
      formulasShortcutList.innerHTML = "";
    }
    if (formulasMistakeList) {
      formulasMistakeList.innerHTML = "";
    }
    return;
  }
  if (formulasFormulaList) {
    formulasFormulaList.innerHTML = groups.map((group) => `
      <section class="formula-section">
        <div class="formula-card-meta">
          <span class="pill">${escapeHtml(formulaSubjectLabel(group.chapter.subject))}</span>
          <strong>${escapeHtml(group.chapter.name)}</strong>
        </div>
        <div class="formula-card-list">${group.formulas.map((formula) => renderFormulaCard(formula, query)).join("")}</div>
      </section>
    `).join("");
  }
  if (formulasShortcutList) {
    const shortcuts = groups.flatMap((group) => group.shortcuts.map((shortcut) => ({ shortcut, chapter: group.chapter })));
    formulasShortcutList.innerHTML = shortcuts.length
      ? shortcuts.map(({ shortcut, chapter }) => `
        <article class="formula-shortcut-card">
          <p class="card-title">${highlightFormulaMatch(shortcut.title || "Shortcut", query)}</p>
          <p class="muted">${escapeHtml(chapter.name)} - ${highlightFormulaMatch(shortcut.detail || "", query)}</p>
        </article>
      `).join("")
      : "";
  }
  if (formulasMistakeList) {
    formulasMistakeList.innerHTML = "";
  }
}

function renderFormulaDetail() {
  const query = formulasSearchInput ? formulasSearchInput.value.trim() : "";
  if (query) {
    renderFormulaSearchResults(query);
    return;
  }
  const chapter = formulaChapters.find((item) => formulaChapterKey(item) === selectedFormulaChapterKey) || formulaChapters[0];
  renderFormulaChapterDetail(chapter);
}

function collectFormulaWeakTerms(payload) {
  const terms = new Set();
  const addTerm = (value) => {
    const term = normalizeFormulaTerm(value);
    if (term) {
      terms.add(term);
    }
  };
  const weakStrong = payload && payload.weak_strong ? payload.weak_strong : {};
  const candidates = [
    weakStrong.weak_topics,
    weakStrong.weak_chapters,
    weakStrong.needs_focus,
    weakStrong.revision_topics,
    payload && payload.weak_topics,
  ];
  candidates.forEach((candidate) => {
    if (Array.isArray(candidate)) {
      candidate.forEach((item) => {
        if (typeof item === "string") {
          addTerm(item);
        } else if (item && typeof item === "object") {
          addTerm(item.topic || item.chapter || item.name || item.unit_name || item.title);
        }
      });
    } else if (candidate && typeof candidate === "object") {
      Object.values(candidate).forEach((value) => addTerm(value));
    }
  });
  return terms;
}

async function loadFormulaWeakTopics() {
  if (!activeProfile || !formulasWeakToggle || !formulasWeakToggle.checked) {
    return;
  }
  const studentName = activeProfile.name || activeProfile.student_id || "";
  if (!studentName || formulaWeakLoadedFor === studentName) {
    return;
  }
  try {
    const response = await fetch(`/api/analytics/dashboard/${encodeURIComponent(studentName)}`);
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Could not load weak topics.");
    }
    formulaWeakTopicTerms = collectFormulaWeakTerms(payload);
    formulaWeakLoadedFor = studentName;
  } catch (error) {
    console.warn("Could not load weak topics for formulas:", error);
    setFormulasStatus("Could not reorder weak topics right now.");
  }
}

function downloadFormulaChapterPdf() {
  const chapter = formulaChapters.find((item) => formulaChapterKey(item) === selectedFormulaChapterKey) || formulaChapters[0];
  if (!chapter) {
    return;
  }
  const formulas = (chapter.formulas || []).map((formula) => {
    const variables = formula.variables && typeof formula.variables === "object"
      ? Object.entries(formula.variables).map(([key, value]) => `${key}: ${value}`).join("\n")
      : "";
    return `${formula.name}\n${formula.formula}\n${variables}\nCondition: ${formula.condition || "-"}\nJEE Tip: ${formula.jee_tip || "-"}\nQuick memory: ${formula.quick_memory || "-"}`;
  }).join("\n\n");
  const shortcuts = (chapter.shortcuts || []).map((shortcut) => `${shortcut.title}: ${shortcut.detail}`).join("\n");
  const mistakes = (chapter.common_mistakes || []).map((mistake) => `- ${mistake}`).join("\n");
  const printable = `
    <html>
      <head><title>${escapeHtml(chapter.name)} Formulas</title></head>
      <body>
        <pre style="font-family: Arial, sans-serif; white-space: pre-wrap; line-height: 1.5;">
${escapeHtml(`${chapter.name} (${formulaSubjectLabel(chapter.subject)})
JEE weightage: ${chapter.jee_weightage || 0}%

FORMULAS

${formulas}

SHORTCUTS

${shortcuts || "-"}

COMMON MISTAKES

${mistakes || "-"}`)}
        </pre>
        <script>window.print();</script>
      </body>
    </html>
  `;
  const printWindow = window.open("", "_blank");
  if (!printWindow) {
    showToast("Allow popups to download this formula sheet as PDF.", "warning");
    return;
  }
  printWindow.document.write(printable);
  printWindow.document.close();
}

function renderMarkdownElement(element, text) {
  if (!element) {
    return;
  }
  const source = normalizeTutorMathText(text).trim();
  if (!source) {
    element.textContent = "";
    return;
  }
  if (window.marked && typeof window.marked.parse === "function") {
    window.marked.setOptions({ breaks: true, gfm: true });
    element.innerHTML = window.marked.parse(source);
    return;
  }
  element.textContent = source;
}

function normalizePracticeReply(text) {
  if (!text) {
    return "";
  }

  let formatted = String(text).trim();
  formatted = formatted.replace(/\r\n/g, "\n");
  formatted = formatted.replace(/(Time Limit:|Instructions:|Questions:|Answer Format:|Answer Key:|Section [A-Z]:|Section \d+:)/gi, "\n$1");
  formatted = formatted.replace(/(\d+\.\s+)/g, "\n$1");
  formatted = formatted.replace(/(Question\s+\d+:)/gi, "\n$1");
  formatted = formatted.replace(/\n{3,}/g, "\n\n");
  return formatted.trim();
}

async function streamTutorReply(mode, text) {
  const preparedText = mode === "practice" ? normalizePracticeReply(text) : text;
  const textEnabled = mode !== "tutor" || (showTextExplanation ? showTextExplanation.checked : true);
  const paragraph = appendMessage(mode, "tutor", textEnabled ? "" : "Text explanation hidden. Video and reasoning panels are still active.");
  if (!paragraph || !textEnabled) {
    if (mode === "tutor" && autoCaptionMode.checked) {
      setCaption(preparedText);
    }
    return;
  }

  const chunks = preparedText.match(/\S+|\s+/g) || [];
  const narration = {
    id: `${mode}-${Date.now()}`,
    mode,
    paragraph,
    chunks,
    output: "",
    index: 0,
    paused: false,
    cancelled: false,
    text: preparedText,
    checkpoint: preparedText,
    resumed: false,
    voiceStarted: false,
  };
  activeTutorNarration = narration;
  updateTutorRoomLivePanel();

  const updateResumeControls = () => {
    if (pauseVoiceBtn) {
      pauseVoiceBtn.textContent = narration.paused ? "Paused" : "Pause reply";
      pauseVoiceBtn.disabled = narration.cancelled || narration.index >= narration.chunks.length;
    }
    if (resumeVoiceBtn) {
      resumeVoiceBtn.disabled = !narration.paused;
    }
  };

  updateResumeControls();
  const activeTabId = document.querySelector(".tab-panel.active")?.id || "";
  const stepDelay = 22;
  while (narration.index < narration.chunks.length) {
    if (narration.cancelled) {
      break;
    }
    if (narration.paused) {
      await new Promise((resolve) => window.setTimeout(resolve, 80));
      continue;
    }
    narration.output += narration.chunks[narration.index];
    paragraph.textContent = narration.output;
    if (mode === "tutor" && autoCaptionMode.checked) {
      setCaption(narration.output);
    }
    const feed = getFeedForMode(mode);
    if (feed) {
      feed.scrollTop = feed.scrollHeight;
    }
    syncTutorFullscreenOverlay();
    narration.index += 1;
    updateResumeControls();
    await new Promise((resolve) => window.setTimeout(resolve, stepDelay));
  }

  if (!narration.cancelled && narration.index >= narration.chunks.length) {
    narration.paused = false;
    narration.resumed = false;
    // MARKED RENDERING FIXED
    window.marked.setOptions({ breaks: true, gfm: true });
    paragraph.innerHTML = marked.parse(normalizeTutorMathText(narration.output || ""));
    if (mode === "tutor" && autoCaptionMode.checked) {
      setCaption(narration.output || preparedText);
    }
    syncTutorFullscreenOverlay();
    saveTutorCheckpoint(mode, preparedText, narration.output || preparedText);
  }
    if (activeTutorNarration === narration) {
      activeTutorNarration = narration.cancelled ? narration : null;
    }
    updateResumeControls();
    updateTutorRoomLivePanel();
    if (mode === "tutor") {
      onTutorReplyReceived(preparedText);
    }
  }

function setActiveTab(tabId) {
  if (tabId === "progressTab") {
    pendingPlanSubtab = "progress";
    tabId = "weeklyTab";
  }
  keepTabPanelNearTop(tabId);
  if (tabId !== "loungeTab") {
    stopLoungeVoiceInput();
  }
  const tabSectionMap = {
    overviewTab: "home",
    tutorTab: "learn",
    videoTutorTab: "learn",
    formulasTab: "learn",
    practiceTab: "learn",
    mockTestTab: "learn",
    lastMinuteTab: "learn",
    tipsTab: "learn",
    weeklyTab: "plan",
    progressTab: "plan",
    loungeTab: "connect",
    networkTab: "connect",
    leagueTab: "connect",
    personalizeTab: "settings",
    guideTab: "settings",
    assistTab: "settings",
  };
  setActiveSectionGroup(tabSectionMap[tabId] || "home", { skipTabSwitch: true });
  if (tabId === "leagueTab" && !isLeagueTabEnabled()) {
    tabId = "overviewTab";
    keepTabPanelNearTop(tabId);
  }
    if (tabId === "videoTutorTab" && activeStudioPane !== "threeConceptPanel") {
      setActiveStudioPane("threeConceptPanel");
    }
    if (tabId === "weeklyTab" && activeProfile) {
      window.setTimeout(() => {
        refreshWeeklyPlan();
        refreshJourneyDashboard();
        refreshActiveChapterSession();
    }, 0);
  }
  if (tabId === "mockTestTab" && activeProfile) {
    window.setTimeout(() => {
      void loadMockCatalogue();
      void loadMockHistory();
    }, 0);
  }
  if (tabId === "formulasTab") {
    window.setTimeout(() => {
      void loadFormulaDatabase();
    }, 0);
  }
  if (tabId !== "mockTestTab") {
    lastNonMockTabId = tabId;
  }
  refreshTabCollections();
  tabButtons.forEach((button) => {
    const isActive = button.dataset.tab === tabId;
    button.classList.toggle("active", isActive);
    button.setAttribute("aria-selected", String(isActive));
  });

  tabPanels.forEach((panel) => {
    panel.classList.toggle("active", panel.id === tabId);
  });
  scrollActivePanelToTop(tabId);
  updateContextPanel(tabId);
  if (tabId === "overviewTab") {
    void loadDailyBriefingIfNeeded();
    updateOverviewCommandCenter();
  }

  if (tabId === "overviewTab") {
    setHomeSubtab("overview");
  }

  if (tabId === "weeklyTab") {
    const nextPlanSubtab = pendingPlanSubtab || "today";
    pendingPlanSubtab = "";
    setPlanSubtab(nextPlanSubtab);
  }

  if (tabId === "tutorTab" && messageInput) {
    window.setTimeout(() => messageInput.focus(), 0);
    if (activeProfile) {
      window.setTimeout(() => {
        void refreshActiveChapterSession();
        void loadChapterResumeState();
      }, 0);
    }
  } else if (tabId === "videoTutorTab" && videoTutorQuestionInput) {
    window.setTimeout(() => videoTutorQuestionInput.focus(), 0);
    window.setTimeout(() => {
      initVideoSearch();
      void loadVideoTutorWorkspace();
      ensureWelcomeTutorVideoLoaded();
    }, 0);
  }
  if (tabId === "tutorTab") {
    renderTutorSmartPrompts();
    updateTutorInputTopicChip();
    updateTutorSuggestedPromptsVisibility();
    syncTutorControlStrip();
    if (!tutorSidePanelCollapsed) {
      setTutorSidePanelTab(activeTutorSideTab || "session");
    }
  }
  updateTutorRoomLivePanel();
}

function applyAccessibilityPreferences() {
  document.body.classList.toggle("high-contrast", highContrastMode.checked);
  document.body.classList.toggle("large-text", largeTextMode.checked);
  document.body.classList.toggle("reduced-motion", reducedMotionMode.checked);
  document.body.classList.toggle("reading-comfort", readingComfortMode && readingComfortMode.checked);
  document.body.classList.toggle("chunked-replies", chunkedReplyMode && chunkedReplyMode.checked);
  const pacingMode = (responsePacingSelect && responsePacingSelect.value) || "standard";
  document.body.classList.toggle("slow-pacing", pacingMode === "slow");
  document.body.classList.toggle("gentle-pacing", pacingMode === "gentle");

  localStorage.setItem("alt_high_contrast", highContrastMode.checked ? "1" : "0");
  localStorage.setItem("alt_large_text", largeTextMode.checked ? "1" : "0");
  localStorage.setItem("alt_reduced_motion", reducedMotionMode.checked ? "1" : "0");
  localStorage.setItem("alt_reading_comfort", readingComfortMode && readingComfortMode.checked ? "1" : "0");
  localStorage.setItem("alt_chunked_replies", chunkedReplyMode && chunkedReplyMode.checked ? "1" : "0");
  localStorage.setItem("alt_response_pacing", pacingMode);
  localStorage.setItem("alt_auto_caption", autoCaptionMode.checked ? "1" : "0");
  localStorage.setItem("alt_auto_speak", autoSpeakReplies.checked ? "1" : "0");
  localStorage.setItem("alt_voice_chat_mode", voiceChatMode && voiceChatMode.checked ? "1" : "0");
}

function applyThemePreferences() {
  document.body.dataset.theme = currentTheme;
  document.body.dataset.background = currentBackground;
  document.body.classList.toggle("night-mode", currentTheme === "midnight");
  localStorage.setItem("alt_theme", currentTheme);
  localStorage.setItem("alt_background", currentBackground);
  localStorage.setItem("alt_night_mode", currentTheme === "midnight" ? "1" : "0");
  if (nightModeToggle) {
    nightModeToggle.checked = currentTheme === "midnight";
  }

  document.querySelectorAll("[data-theme]").forEach((button) => {
    button.classList.toggle("active", button.dataset.theme === currentTheme);
  });
  document.querySelectorAll("[data-background]").forEach((button) => {
    button.classList.toggle("active", button.dataset.background === currentBackground);
  });
}

function loadAccessibilityPreferences() {
  highContrastMode.checked = localStorage.getItem("alt_high_contrast") === "1";
  largeTextMode.checked = localStorage.getItem("alt_large_text") === "1";
  reducedMotionMode.checked = localStorage.getItem("alt_reduced_motion") === "1";
  if (readingComfortMode) {
    readingComfortMode.checked = localStorage.getItem("alt_reading_comfort") === "1";
  }
  if (chunkedReplyMode) {
    chunkedReplyMode.checked = localStorage.getItem("alt_chunked_replies") !== "0";
  }
  if (responsePacingSelect) {
    const storedPacing = localStorage.getItem("alt_response_pacing");
    responsePacingSelect.value = ["standard", "gentle", "slow"].includes(storedPacing) ? storedPacing : "gentle";
  }
  autoCaptionMode.checked = localStorage.getItem("alt_auto_caption") !== "0";
  autoSpeakReplies.checked = localStorage.getItem("alt_auto_speak") === "1";
  if (voiceChatMode) {
    voiceChatMode.checked = localStorage.getItem("alt_voice_chat_mode") === "1";
  }
  const storedTheme = localStorage.getItem("alt_theme");
  currentTheme = storedTheme && storedTheme !== "sunrise" ? storedTheme : "midnight";
  if (localStorage.getItem("alt_night_mode") === "1") {
    currentTheme = "midnight";
  }
  currentBackground = localStorage.getItem("alt_background") || "glow";
  currentLanguage = normalizeLanguageSelection(localStorage.getItem("alt_language") || "english");
  leagueTabVisible = localStorage.getItem("alt_show_league_tab") !== "0";
  const savedOrder = safeJsonParse(localStorage.getItem("alt_tab_order") || "[]", []);
  const savedOrderList = Array.isArray(savedOrder) ? savedOrder : [];
  const validSavedOrder = savedOrderList.filter((key) => TAB_CONFIG[key] && key !== "progress");
  const missingKeys = Object.keys(TAB_CONFIG).filter((key) => !validSavedOrder.includes(key));
  currentTabOrder = [...validSavedOrder, ...missingKeys];
  currentTabOrder = currentTabOrder.filter((key) => key !== LEGACY_TUTOR_ROOM_KEY);

  if (languageSelect) {
    languageSelect.value = currentLanguage;
  }
  if (nightModeToggle) {
    nightModeToggle.checked = currentTheme === "midnight";
  }
  applyAccessibilityPreferences();
  applyThemePreferences();
  applyLanguage();
  renderTutorLanguageDropdown();
  applyLeagueVisibility();
}


function applySidebarState() {
  if (!appShell) {
    return;
  }
  appShell.classList.toggle("sidebar-collapsed", !!isSidebarCollapsed);
  if (studioMenuToggleBtn) {
    studioMenuToggleBtn.textContent = isSidebarCollapsed ? "Show studio menu" : "Hide studio menu";
  }
  localStorage.setItem("alt_sidebar_collapsed", isSidebarCollapsed ? "1" : "0");
}

function loadSidebarPreference() {
  isSidebarCollapsed = localStorage.getItem("alt_sidebar_collapsed") === "1";
  applySidebarState();
}

function loadStudioPanePreference() {
  const savedPane = localStorage.getItem("alt_studio_pane");
  const validPane = studioPanes.find((pane) => pane.id === savedPane);
  setActiveStudioPane(validPane ? savedPane : "threeConceptPanel");
}

function persistAuthSession(session, user) {
  authSession = session || null;
  activeUser = user || null;
  if (session && session.access_token) {
    localStorage.setItem("alt_auth_token", session.access_token);
  } else {
    localStorage.removeItem("alt_auth_token");
  }
  if (user) {
    localStorage.setItem("alt_auth_user", JSON.stringify(user));
  } else {
    localStorage.removeItem("alt_auth_user");
  }
}

function getAuthHeaders() {
  const token = localStorage.getItem("alt_auth_token");
  return token
    ? {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      }
    : {
        "Content-Type": "application/json",
      };
}

window.getAuthHeaders = getAuthHeaders;

function resetClientSessionState(message = "Sign in or create a fresh JEE account to continue.") {
  persistAuthSession(null, null);
  activeProfile = null;
  activeTutorConversationId = null;
  activeLoungeConversationId = null;
  activeTutorVideo = null;
  videoLibrarySnapshot = null;
  lastTutorReply = "";
  lastTutorQuestion = "";
  lastVideoAnswerBrief = null;
  activeTutorVideoJobId = "";
  if (activeTutorVideoPollInterval) {
    window.clearInterval(activeTutorVideoPollInterval);
    activeTutorVideoPollInterval = null;
  }
  activeChapterResumeSummary = null;
  chapterResumeLoadedFor = "";
  chapterResumeDismissedFor = "";
  activeChapterSession = null;
  activeChapterSubtopic = null;
  activeChapterTest = null;
  activeHomeSubtab = "overview";
  clearChapterTimers();
  hideChapterResumeUI();
  if (chapterCompletionCard) {
    chapterCompletionCard.classList.add("hidden");
    chapterCompletionCard.innerHTML = "";
  }
  clearChapterTestContainer();
  lastRepliesByMode = { tutor: "", guide: "", lounge: "", practice: "", last_minute: "", tips: "" };
  loginScreen.classList.remove("hidden");
  if (introScreen) {
    introScreen.classList.add("hidden");
  }
  appShell.classList.add("hidden");
  profileStatus.textContent = "Sign in or create a fresh JEE account to continue.";
  if (signinPasswordInput) {
    signinPasswordInput.value = "";
  }
  renderStorageStatus(null);
  renderTutorConversations([]);
  renderDeletedTutorConversations([]);
  renderLoungeConversations([]);
  renderDeletedLoungeConversations([]);
  renderVideoLibrary(null);
  renderVideoAnswerBrief(null);
  setVideoTutorStatus("Astra is waiting for a video answer request.", { visible: true });
  if (tutorVideoAnswerPlayer) {
    tutorVideoAnswerPlayer.pause();
    tutorVideoAnswerPlayer.removeAttribute("src");
    tutorVideoAnswerPlayer.load();
    tutorVideoAnswerPlayer.classList.add("hidden");
  }
  if (videoTranscriptPanel) {
    videoTranscriptPanel.textContent = "";
  }
  setVideoTutorStatus("Astra is waiting for a video answer request.", { visible: true });
  renderAuthHeroVideo(authHeroVideoSnapshot || videoLibrarySnapshot || null);
  if (introVideoPlayer) {
    introVideoPlayer.pause();
    introVideoPlayer.muted = true;
  }
  setAuthMode("signin");
  renderDailyMotivation("");
  setHomeSubtab("overview");
  setTutorMode("calm");
  profileStatus.textContent = message;
}

async function logoutAndShowAuth() {
  const token = localStorage.getItem("alt_auth_token");
  try {
    if (token) {
      await fetch("/api/auth/logout", {
        method: "POST",
        headers: getAuthHeaders(),
      });
    }
  } catch (error) {
    console.warn("Could not notify backend about logout:", error);
  }
  resetClientSessionState("Sign in or create a fresh JEE account to continue.");
  window.location.reload();
}

function handleSessionExpired(message = "Your session has expired. Please sign in again.") {
  resetClientSessionState(message);
}

window.handleSessionExpired = handleSessionExpired;

async function restoreSessionIfAvailable() {
  const token = localStorage.getItem("alt_auth_token");
  if (!token) {
    return;
  }

  try {
    const response = await fetch("/api/auth/me", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    const payload = await response.json();
    if (!response.ok) {
      persistAuthSession(null, null);
      return;
    }

    persistAuthSession({ access_token: token, token_type: "bearer" }, payload.user || null);
    await enterLearningStudio((payload.profile && payload.profile.name) || (payload.user && payload.user.student_name) || "", { introMode: "signin" });
  } catch (error) {
    persistAuthSession(null, null);
  }
}

function applyLanguage() {
  const normalizedLanguage = normalizeLanguageSelection(currentLanguage);
  currentLanguage = normalizedLanguage;
  window.astraLanguage = normalizedLanguage;
  localStorage.setItem("alt_language", normalizedLanguage);
  if (languageBadge) {
    languageBadge.textContent = getLanguageDisplayLabel(normalizedLanguage);
  }
  if (languageSelect) {
    languageSelect.value = normalizedLanguage;
  }
  updateTutorLanguageChip();
  updateLanguageSelectionCards();
  updateHinglishToggleState();
}

const LANGUAGE_OPTIONS = [
  { key: "english", native: "English", label: "English (Default)" },
  { key: "hindi", native: "Hindi", label: "Hindi" },
  { key: "hinglish", native: "Hinglish", label: "Hindi + English" },
  { key: "telugu", native: "Telugu", label: "Telugu" },
  { key: "tamil", native: "Tamil", label: "Tamil" },
  { key: "kannada", native: "Kannada", label: "Kannada" },
  { key: "marathi", native: "Marathi", label: "Marathi" },
  { key: "bengali", native: "Bengali", label: "Bengali" },
  { key: "gujarati", native: "Gujarati", label: "Gujarati" },
];

function normalizeLanguageSelection(language) {
  const value = String(language || "").trim().toLowerCase();
  if (!value) {
    return "english";
  }
  const aliases = {
    english: "english",
    eng: "english",
    hindi: "hindi",
    hinglish: "hinglish",
    "hindi + english": "hinglish",
    "hindi english": "hinglish",
    telugu: "telugu",
    tamil: "tamil",
    kannada: "kannada",
    marathi: "marathi",
    bengali: "bengali",
    gujarati: "gujarati",
  };
  const supportedKeys = ["english", "hindi", "hinglish", "telugu", "tamil", "kannada", "marathi", "bengali", "gujarati"];
  return aliases[value] || (supportedKeys.includes(value) ? value : "english");
}

function getLanguageDisplayLabel(language) {
  const normalized = normalizeLanguageSelection(language);
  return (LANGUAGE_OPTIONS.find((entry) => entry.key === normalized) || LANGUAGE_OPTIONS[0]).label;
}

function getLanguageNativeLabel(language) {
  const normalized = normalizeLanguageSelection(language);
  return (LANGUAGE_OPTIONS.find((entry) => entry.key === normalized) || LANGUAGE_OPTIONS[0]).native;
}

function updateTutorLanguageChip() {
  if (!tutorLanguageChip) {
    return;
  }
  tutorLanguageChip.textContent = getLanguageDisplayLabel(currentLanguage).replace(" (Default)", "");
}

function updateLanguageSelectionCards() {
  if (!tutorLanguageSelector) {
    return;
  }
  const selectedLanguage = normalizeLanguageSelection(currentLanguage);
  tutorLanguageSelector.querySelectorAll(".language-card").forEach((card) => {
    const cardLanguage = normalizeLanguageSelection(card.dataset.language);
    card.classList.toggle("selected", cardLanguage === selectedLanguage);
  });
}

function updateHinglishToggleState() {
  if (!hinglishToggle) {
    return;
  }
  const isHinglish = normalizeLanguageSelection(currentLanguage) === "hinglish";
  hinglishToggle.textContent = isHinglish ? "Disable Hinglish" : "Enable Hinglish";
}

function renderTutorLanguageDropdown() {
  if (!tutorLanguageDropdown) {
    return;
  }
  tutorLanguageDropdown.innerHTML = LANGUAGE_OPTIONS.map((option) => (
    `<button type="button" data-language-option="${option.key}">${option.native} - ${option.label.replace(" (Default)", "")}</button>`
  )).join("");
}

async function setLanguagePreference(language, { persist = true, updateProfile = true, showConfirmation = true } = {}) {
  const normalizedLanguage = normalizeLanguageSelection(language);
  currentLanguage = normalizedLanguage;
  window.astraLanguage = normalizedLanguage;
  applyLanguage();
  let saveSucceeded = !persist || !activeProfile;
  if (persist && activeProfile) {
    try {
      const response = await fetch("/api/profile/set-language", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          student_id: activeProfile.name,
          preferred_language: normalizedLanguage,
          ui_language: normalizedLanguage,
        }),
      });
      const payload = await response.json();
      if (response.ok && payload.profile) {
        activeProfile = payload.profile;
        saveSucceeded = true;
        if (updateProfile) {
          updateTutorSummary(activeProfile);
        }
      }
    } catch (error) {
      console.warn("Could not save language preference:", error);
      saveSucceeded = false;
    }
  }
  if (showConfirmation) {
    showToast(
      saveSucceeded
        ? `Astra will now explain in ${getLanguageDisplayLabel(normalizedLanguage).replace(" (Default)", "")}.`
        : "Could not save language preference right now.",
      saveSucceeded ? "success" : "warning"
    );
  }
}

const WALKTHROUGH_STEPS = [
  {
    key: "intro",
    type: "intro",
    prompt: "Welcome to Astra.",
      helper:
      "Astra begins with a guided walk so it can understand your goals, comfort, and interests before tutoring starts. Your answers become Astra's starting defaults for the app, and you can change them anytime in Personalize. You will answer the short questions below and then get one final chance to ask Astra anything. This is not an interview. It is the first step in building a real connection.",
    placeholder: "",
  },
  {
    key: "why_astra",
    prompt: "Why do you want Astra in your corner?",
    helper: "This helps Astra understand what you hope Astra will do for you and what support you want first.",
    placeholder: "Tell Astra what made you choose this mentor.",
  },
  {
    key: "interests",
    prompt: "What do you enjoy outside studies?",
    helper: "Hobbies, music, sports, movies, games, books, or anything that makes you feel like yourself.",
    placeholder: "Share the things you naturally enjoy.",
  },
  {
    key: "dislikes",
    prompt: "What should Astra avoid or never do?",
    helper: "This keeps Astra away from habits, tones, or patterns that make you uncomfortable.",
    placeholder: "Tell Astra what to avoid.",
  },
  {
    key: "conversation_style",
    prompt: "What kind of conversation style feels best to you?",
    helper: "You can say calm, strict, friendly, funny, direct, motivational, or anything else that feels right.",
    placeholder: "Describe the way you want Astra to talk to you.",
  },
  {
    key: "preferred_language",
    prompt: "What language should Astra use by default?",
    helper: "This becomes the starting language for replies, summaries, and voice when Astra can support it.",
    placeholder: "Tell Astra the language you are most comfortable with.",
  },
  {
    key: "explanation_depth",
    prompt: "How detailed should Astra be by default?",
    helper: "This helps Astra choose short, balanced, or deep explanations whenever it starts a new conversation.",
    placeholder: "Tell Astra whether you want short, balanced, or deep answers.",
  },
  {
    key: "stress_support",
    prompt: "What helps you when you feel stressed or overloaded?",
    helper: "This helps Astra know when to slow down, reassure you, push gently, or give you a break.",
    placeholder: "Tell Astra what support feels best when you are under pressure.",
  },
  {
    key: "goals_summary",
    prompt: "When do you learn best?",
    helper: "Tell Astra about the environment, time, pace, and conditions where you actually understand things well, trust the process, and start enjoying learning.",
    placeholder: "Describe the situations where learning feels natural for you.",
  },
  {
    key: "astra_question",
    prompt: "Do you have any doubts about Astra or the website?",
    helper: "You can ask how Astra works, how it learns, how it stays private, or anything else you want to clear before starting.",
    placeholder: "Ask Astra anything about the app, the tutor, or the website.",
  },
];

function buildWalkthroughAstraAnswer(question) {
  const text = String(question || "").toLowerCase();
  if (!text) {
    return "Ask me anything about how Astra works, and I'll answer in a simple, honest way.";
  }
  if (text.includes("private") || text.includes("privacy")) {
    return "Astra only uses what you choose to share, and you can change or remove those settings later.";
  }
  if (text.includes("tutor") || text.includes("teach")) {
    return "Tutor stays academic, Lounge stays casual, Practice stays drill-focused, and your planner adapts from your profile defaults.";
  }
  if (text.includes("learn") || text.includes("adapt")) {
    return "Astra learns from the answers you give, your progress, your behavior signals, and the way you use the app so the defaults feel personal.";
  }
  if (text.includes("group") || text.includes("friends")) {
    return "Group study is opt-in. You can study solo, study with friends, or use matched study rooms and switch back anytime.";
  }
  if (text.includes("change") || text.includes("later")) {
    return "Yes, you can edit these answers later in Personalize, so the setup can evolve with you.";
  }
  if (text.includes("why") || text.includes("what is")) {
    return "Astra is built to understand your style first, then use those answers as the starting defaults for tutoring, planning, and support in a way that feels personal.";
  }
  return "Astra is meant to be a mentor-companion: personal, academic, and easy to adjust as you learn what works best for you.";
}

function applyWalkthroughAnswersToSignupFields() {
  if (signupWhyAstra) {
    signupWhyAstra.value = walkthroughAnswers.why_astra || "";
  }
  if (signupInterests) {
    signupInterests.value = walkthroughAnswers.interests || "";
  }
  if (signupDislikes) {
    signupDislikes.value = walkthroughAnswers.dislikes || "";
  }
  if (signupConversationStyle) {
    signupConversationStyle.value = walkthroughAnswers.conversation_style || "";
  }
  if (signupStressSupport) {
    signupStressSupport.value = walkthroughAnswers.stress_support || "";
  }
  if (signupGoalsSummary) {
    signupGoalsSummary.value = walkthroughAnswers.goals_summary || "";
  }
}

function inferTutorLevelFromExplanationDepth(depthText) {
  const text = String(depthText || "").toLowerCase();
  if (!text) {
    return 3;
  }
  if (text.includes("short") || text.includes("brief") || text.includes("quick")) {
    return 1;
  }
  if (text.includes("simple") || text.includes("easy")) {
    return 2;
  }
  if (text.includes("deep") || text.includes("detailed") || text.includes("expert")) {
    return 5;
  }
  if (text.includes("balanced") || text.includes("normal") || text.includes("medium")) {
    return 3;
  }
  return 3;
}

function applyOnboardingDefaultsToApp(profile) {
  if (!profile) {
    return;
  }

  const onboarding = profile.onboarding_profile || {};
  const preferredLanguage = normalizeLanguageSelection(
    profile.preferred_language || profile.ui_language || profile.default_response_language || onboarding.preferred_language || currentLanguage
  );
  if (preferredLanguage) {
    currentLanguage = preferredLanguage;
    if (languageSelect) {
      languageSelect.value = currentLanguage;
    }
    applyLanguage();
  }

  const defaultTutorLevel = Number(profile.default_tutor_level || inferTutorLevelFromExplanationDepth(onboarding.explanation_depth));
  if (tutorLevelSelect && defaultTutorLevel) {
    tutorLevelSelect.value = String(defaultTutorLevel);
    updateTutorLevelHint();
  }

  updateExamBrandCopy(profile);
}

function populateWalkthroughFromProfile(profile) {
  const onboarding = (profile && profile.onboarding_profile) || {};
  walkthroughAnswers = {
    why_astra: onboarding.why_astra || "",
    interests: onboarding.interests || "",
    dislikes: onboarding.dislikes || "",
    conversation_style: onboarding.conversation_style || "",
    preferred_language: onboarding.preferred_language || "",
    explanation_depth: onboarding.explanation_depth || "",
    stress_support: onboarding.stress_support || "",
    goals_summary: onboarding.goals_summary || "",
    astra_question: onboarding.astra_question || "",
    astra_question_answer: onboarding.astra_question_answer || "",
  };
}

function setWalkthroughAnswerText(text) {
  if (walkthroughAstraAnswer) {
    walkthroughAstraAnswer.textContent = text;
  }
}

function resetWalkthroughParticle(node, forceDelay = false) {
  const lane = Math.random() > 0.5 ? 1 : -1;
  const depth = 0.25 + Math.random() * 0.75;
  const spread = 60 + Math.random() * 220;
  const rise = -45 - Math.random() * 180;
  const size = 6 + Math.random() * 14;
  node.state = {
    x: (Math.random() - 0.5) * 120,
    y: (Math.random() - 0.5) * 120,
    lane,
    depth,
    spread,
    rise,
    size,
    life: 180 + Math.random() * 160,
    age: forceDelay ? Math.random() * 120 : 0,
  };
  node.el.style.width = `${size}px`;
  node.el.style.height = `${size}px`;
}

function updateWalkthroughParticles() {
  if (!walkthroughParticles || !walkthroughParticleNodes.length) {
    walkthroughParticleFrame = null;
    return;
  }

  walkthroughParticleNodes.forEach((node) => {
    const state = node.state;
    state.age += 1;
    if (state.age >= state.life) {
      resetWalkthroughParticle(node, true);
      return;
    }

    const progress = state.age / state.life;
    const drift = progress * progress;
    const outward = state.spread * progress * 1.5;
    const horizontal = state.x + (outward + 24 * progress) * state.lane;
    const vertical = state.y + state.rise * progress - 38 * drift;
    const depthShift = -260 * progress - 48 * Math.sin(progress * Math.PI);
    const scale = Math.max(0.16, 1 - progress * 0.8);
    const opacity = progress < 0.16 ? progress / 0.16 : progress > 0.82 ? Math.max(0, (1 - progress) / 0.18) : 1;

    node.el.style.transform = `translate3d(${horizontal}px, ${vertical}px, ${depthShift}px) scale(${scale})`;
    node.el.style.opacity = `${opacity}`;
  });

  walkthroughParticleFrame = window.requestAnimationFrame(updateWalkthroughParticles);
}

function startWalkthroughParticles() {
  if (!walkthroughParticles) {
    return;
  }

  walkthroughParticles.innerHTML = "";
  walkthroughParticleNodes = [];
  const count = window.matchMedia("(max-width: 760px)").matches ? 32 : 64;
  for (let index = 0; index < count; index += 1) {
    const el = document.createElement("span");
    el.className = "walkthrough-particle";
    walkthroughParticles.appendChild(el);
    const node = { el, state: null };
    resetWalkthroughParticle(node, index > 0);
    walkthroughParticleNodes.push(node);
  }

  if (walkthroughParticleFrame) {
    window.cancelAnimationFrame(walkthroughParticleFrame);
  }
  walkthroughParticleFrame = window.requestAnimationFrame(updateWalkthroughParticles);
}

function stopWalkthroughParticles() {
  if (walkthroughParticleFrame) {
    window.cancelAnimationFrame(walkthroughParticleFrame);
    walkthroughParticleFrame = null;
  }
  walkthroughParticleNodes = [];
  if (walkthroughParticles) {
    walkthroughParticles.innerHTML = "";
  }
}

function renderWalkthroughStepLegacy() {
  if (!walkthroughModal) {
    return;
  }
  const step = WALKTHROUGH_STEPS[walkthroughStepIndex] || WALKTHROUGH_STEPS[0];
  if (walkthroughStepLabel) {
    walkthroughStepLabel.textContent = `Step ${walkthroughStepIndex + 1}`;
  }
  if (walkthroughStepCount) {
    walkthroughStepCount.textContent = `${walkthroughStepIndex + 1} of ${WALKTHROUGH_STEPS.length}`;
  }
  if (walkthroughPrompt) {
    walkthroughPrompt.textContent = step.prompt;
  }
  if (walkthroughHelper) {
    walkthroughHelper.textContent = step.helper;
  }
  if (walkthroughInput) {
    walkthroughInput.value = walkthroughAnswers[step.key] || "";
    walkthroughInput.placeholder = step.placeholder || "Type your answer here...";
  }
  if (walkthroughModePill) {
    walkthroughModePill.textContent = walkthroughContext === "signup" ? "New user" : "Saved profile";
  }
  if (walkthroughSaveBtn) {
    walkthroughSaveBtn.textContent = walkthroughContext === "signup" ? "Save to sign up" : "Save answers";
  }
  if (walkthroughNextBtn) {
    walkthroughNextBtn.textContent = walkthroughStepIndex === WALKTHROUGH_STEPS.length - 1 ? "Finish" : "Next";
  }
  if (walkthroughBackBtn) {
    walkthroughBackBtn.disabled = walkthroughStepIndex === 0;
  }
  setWalkthroughAnswerText("Ask Astra a question about how it works, and I'll answer it here.");
}

function renderWalkthroughStep() {
  if (!walkthroughModal) {
    return;
  }
  const step = WALKTHROUGH_STEPS[walkthroughStepIndex] || WALKTHROUGH_STEPS[0];
  const isIntro = step.type === "intro";
  const isAstraQuestion = step.key === "astra_question";
  const stageClass = isIntro ? "walkthrough-stage-intro" : "walkthrough-stage-question";
  const questionNumber = Math.max(0, walkthroughStepIndex);
  const totalQuestions = WALKTHROUGH_STEPS.length - 1;

  walkthroughModal.classList.add("walkthrough-stage-transition");
  walkthroughModal.classList.toggle("walkthrough-stage-intro", isIntro);
  walkthroughModal.classList.toggle("walkthrough-stage-question", !isIntro);
  if (walkthroughTransitionTimer) {
    window.clearTimeout(walkthroughTransitionTimer);
  }
  walkthroughTransitionTimer = window.setTimeout(() => {
    if (walkthroughModal) {
      walkthroughModal.classList.remove("walkthrough-stage-transition");
      walkthroughModal.dataset.walkthroughStage = stageClass;
    }
  }, isIntro ? 260 : 320);

  if (walkthroughStepLabel) {
    walkthroughStepLabel.textContent = isIntro ? "Welcome" : isAstraQuestion ? "Final step" : `Question ${questionNumber}`;
  }
  if (walkthroughStepCount) {
    walkthroughStepCount.textContent = isIntro
      ? `${totalQuestions} questions ahead`
      : isAstraQuestion
        ? `Question ${questionNumber} of ${totalQuestions}`
        : `Question ${questionNumber} of ${totalQuestions}`;
  }
  if (walkthroughPrompt) {
    walkthroughPrompt.textContent = isIntro ? step.prompt : `Question ${questionNumber} of ${totalQuestions}: ${step.prompt}`;
  }
  if (walkthroughHelper) {
    walkthroughHelper.textContent = step.helper;
  }
  if (walkthroughInput) {
    walkthroughInput.classList.toggle("hidden", isIntro);
    walkthroughInput.value = isIntro ? "" : (walkthroughAnswers[step.key] || "");
    walkthroughInput.placeholder = step.placeholder || "Type your answer here...";
  }
  if (walkthroughQuestionBlock) {
    walkthroughQuestionBlock.classList.toggle("hidden", isIntro);
  }
  if (walkthroughModePill) {
    walkthroughModePill.textContent = walkthroughContext === "signup" ? "New user" : "Saved profile";
  }
  if (walkthroughSaveBtn) {
    walkthroughSaveBtn.classList.toggle("hidden", isIntro);
    walkthroughSaveBtn.textContent = walkthroughContext === "signup" ? "Save to sign up" : "Save answers";
  }
  if (walkthroughNextBtn) {
    walkthroughNextBtn.textContent = isIntro
      ? "Next"
      : walkthroughStepIndex === WALKTHROUGH_STEPS.length - 1
        ? "Finish"
        : "Next";
  }
  if (walkthroughBackBtn) {
    walkthroughBackBtn.classList.toggle("hidden", isIntro);
    walkthroughBackBtn.disabled = walkthroughStepIndex === 0;
  }
  if (isAstraQuestion && walkthroughAnswers.astra_question_answer) {
    setWalkthroughAnswerText(walkthroughAnswers.astra_question_answer);
  } else if (isIntro) {
    setWalkthroughAnswerText("Read the message, then press Next when you are ready.");
  } else {
    setWalkthroughAnswerText("Ask Astra a question about how it works, and I'll answer it here.");
  }
}

function openWalkthrough(context = "signup", profile = null) {
  walkthroughContext = context === "existing" ? "existing" : "signup";
  walkthroughStepIndex = 0;
  walkthroughProfileSnapshot = profile || activeProfile || null;
  walkthroughAnswers = {
    why_astra: signupWhyAstra ? signupWhyAstra.value.trim() : "",
    interests: signupInterests ? signupInterests.value.trim() : "",
    dislikes: signupDislikes ? signupDislikes.value.trim() : "",
    conversation_style: signupConversationStyle ? signupConversationStyle.value.trim() : "",
    preferred_language: languageSelect ? languageSelect.value.trim() : currentLanguage,
    explanation_depth: tutorLevelSelect ? String(tutorLevelSelect.value || "3") : "3",
    stress_support: signupStressSupport ? signupStressSupport.value.trim() : "",
    goals_summary: signupGoalsSummary ? signupGoalsSummary.value.trim() : "",
    astra_question: "",
    astra_question_answer: "",
  };
  if (walkthroughContext === "existing" && walkthroughProfileSnapshot) {
    populateWalkthroughFromProfile(walkthroughProfileSnapshot);
  }
  if (walkthroughModal) {
    walkthroughModal.classList.remove("hidden");
    walkthroughModal.setAttribute("aria-hidden", "false");
    walkthroughModal.dataset.walkthroughStage = "walkthrough-stage-intro";
    walkthroughModal.scrollTop = 0;
  }
  document.body.classList.add("walkthrough-lock");
  startWalkthroughParticles();
  renderWalkthroughStep();
  if (walkthroughInput) {
    walkthroughInput.focus();
  }
}

function closeWalkthrough() {
  if (walkthroughTransitionTimer) {
    window.clearTimeout(walkthroughTransitionTimer);
    walkthroughTransitionTimer = null;
  }
  if (walkthroughModal) {
    walkthroughModal.scrollTop = 0;
    walkthroughModal.classList.add("hidden");
    walkthroughModal.setAttribute("aria-hidden", "true");
    walkthroughModal.classList.remove("walkthrough-stage-intro", "walkthrough-stage-question", "walkthrough-stage-transition");
  }
  document.body.classList.remove("walkthrough-lock");
  stopWalkthroughParticles();
}

async function saveWalkthroughToExistingProfile() {
  if (!activeProfile) {
    return;
  }
  const payload = {
    student_name: activeProfile.name,
    onboarding_why_astra: walkthroughAnswers.why_astra || "",
    onboarding_interests: walkthroughAnswers.interests || "",
    onboarding_dislikes: walkthroughAnswers.dislikes || "",
    onboarding_conversation_style: walkthroughAnswers.conversation_style || "",
    onboarding_preferred_language: walkthroughAnswers.preferred_language || "",
    onboarding_explanation_depth: walkthroughAnswers.explanation_depth || "",
    onboarding_stress_support: walkthroughAnswers.stress_support || "",
    onboarding_goals_summary: walkthroughAnswers.goals_summary || "",
    onboarding_astra_question: walkthroughAnswers.astra_question || "",
    onboarding_astra_question_answer: walkthroughAnswers.astra_question_answer || "",
    intro_completed: true,
  };
  const response = await fetch("/api/profile/onboarding", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const result = await response.json();
  if (!response.ok) {
    throw new Error(result.detail || "Could not save the Astra walkthrough yet.");
  }
  activeProfile = result.profile || activeProfile;
  applyTutorPersonalityToForm(activeProfile);
  updateTutorSummary(activeProfile);
}

async function saveWalkthrough() {
  const step = WALKTHROUGH_STEPS[walkthroughStepIndex] || WALKTHROUGH_STEPS[0];
  if (walkthroughInput) {
    walkthroughAnswers[step.key] = walkthroughInput.value.trim();
  }
  if (step.key === "astra_question") {
    walkthroughAnswers.astra_question_answer = buildWalkthroughAstraAnswer(walkthroughAnswers.astra_question);
    setWalkthroughAnswerText(walkthroughAnswers.astra_question_answer);
  }
  applyWalkthroughAnswersToSignupFields();
  if (walkthroughContext === "existing" && activeProfile) {
    const response = await fetch("/api/profile/onboarding", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        student_name: activeProfile.name,
        onboarding_why_astra: walkthroughAnswers.why_astra || "",
        onboarding_interests: walkthroughAnswers.interests || "",
        onboarding_dislikes: walkthroughAnswers.dislikes || "",
        onboarding_conversation_style: walkthroughAnswers.conversation_style || "",
        onboarding_preferred_language: walkthroughAnswers.preferred_language || "",
        onboarding_explanation_depth: walkthroughAnswers.explanation_depth || "",
        onboarding_stress_support: walkthroughAnswers.stress_support || "",
        onboarding_goals_summary: walkthroughAnswers.goals_summary || "",
        onboarding_astra_question: walkthroughAnswers.astra_question || "",
        onboarding_astra_question_answer: walkthroughAnswers.astra_question_answer || "",
        intro_completed: true,
      }),
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Could not save the Astra walkthrough yet.");
    }
    activeProfile = payload.profile || activeProfile;
    updateTutorSummary(activeProfile);
    const profileRefresh = await fetch(`/api/profile/${encodeURIComponent(activeProfile.name)}`);
    const profilePayload = await profileRefresh.json();
    if (profileRefresh.ok) {
      renderMemory(profilePayload.personal_memory || {});
      renderMemoryManager(profilePayload.personal_memory || {});
    }
  }
  closeWalkthrough();
}

function advanceWalkthrough(direction) {
  const currentStep = WALKTHROUGH_STEPS[walkthroughStepIndex] || WALKTHROUGH_STEPS[0];
  if (walkthroughInput) {
    walkthroughAnswers[currentStep.key] = walkthroughInput.value.trim();
  }
  if (currentStep.key === "astra_question") {
    walkthroughAnswers.astra_question_answer = buildWalkthroughAstraAnswer(walkthroughAnswers.astra_question);
    setWalkthroughAnswerText(walkthroughAnswers.astra_question_answer);
  }
  walkthroughStepIndex = Math.max(0, Math.min(WALKTHROUGH_STEPS.length - 1, walkthroughStepIndex + direction));
  renderWalkthroughStep();
}

async function askAstraAboutItself() {
  const text = walkthroughInput ? walkthroughInput.value.trim() : "";
  const answer = buildWalkthroughAstraAnswer(text);
  walkthroughAnswers.astra_question = text;
  walkthroughAnswers.astra_question_answer = answer;
  setWalkthroughAnswerText(answer);
}

function updateTutorLevelHint() {
  if (!tutorLevelSelect || !tutorLevelHint) {
    return;
  }
  const level = Number(tutorLevelSelect.value || "3");
  const hints = {
    1: "Level 1 keeps everything simple and in layman terms.",
    2: "Level 2 adds a little more detail while staying easy to follow.",
    3: "Level 3 gives a balanced explanation with clarity and depth.",
    4: "Level 4 goes deeper into the logic and reasoning.",
    5: "Level 5 gives a detailed expert-style explanation for deeper understanding.",
  };
  tutorLevelHint.textContent = hints[level] || hints[3];
}

function setCaption(text) {
  if (!tutorCaptionText) {
    return;
  }
  tutorCaptionText.textContent = autoCaptionMode.checked ? text : "Captions are currently off.";
}

function updateLoungeTimerLabel() {
  if (!loungeTimerStatus) {
    return;
  }

  if (!loungeTimerEndTime) {
    loungeTimerStatus.textContent = "No timer running.";
    return;
  }

  const remainingMs = loungeTimerEndTime - Date.now();
  if (remainingMs <= 0) {
    clearLoungeTimer();
    loungeTimerStatus.textContent = "Time is up. Wrap up the lounge chat and head back when you are ready.";
    appendMessage("lounge", "tutor", "Our casual-talk timer just wrapped up. If you feel lighter now, we can gently move back to what matters next.");
    return;
  }

  const totalSeconds = Math.ceil(remainingMs / 1000);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  loungeTimerStatus.textContent = `Relax timer running: ${minutes}:${String(seconds).padStart(2, "0")} left`;
}

function clearLoungeTimer() {
  if (loungeTimerInterval) {
    window.clearInterval(loungeTimerInterval);
    loungeTimerInterval = null;
  }
  loungeTimerEndTime = null;
}

function startLoungeTimer(minutes) {
  clearLoungeTimer();
  loungeTimerEndTime = Date.now() + minutes * 60 * 1000;
  updateLoungeTimerLabel();
  loungeTimerInterval = window.setInterval(updateLoungeTimerLabel, 1000);
}

function updateLoungeVoiceStatus(text) {
  if (loungeVoiceStatus) {
    loungeVoiceStatus.textContent = text;
  }
}

function setLoungeVoiceButtonState(active) {
  if (!loungeVoiceBtn) {
    return;
  }
  loungeVoiceBtn.textContent = active ? "Stop voice" : "Voice message";
  loungeVoiceBtn.classList.toggle("active", !!active);
  loungeVoiceBtn.setAttribute("aria-pressed", active ? "true" : "false");
}

function stopLoungeVoiceInput() {
  if (loungeVoiceRecognition && loungeVoiceActive) {
    try {
      loungeVoiceRecognition.stop();
    } catch (error) {
      // Ignore stop errors from browsers that cancel recognition on their own.
    }
  }
}

function initLoungeVoiceInput() {
  if (!loungeVoiceBtn) {
    return;
  }

  if (!LoungeSpeechRecognition) {
    loungeVoiceBtn.disabled = true;
    updateLoungeVoiceStatus("Voice messages are not supported in this browser.");
    return;
  }

  loungeVoiceRecognition = new LoungeSpeechRecognition();
  loungeVoiceRecognition.lang = navigator.language || "en-US";
  loungeVoiceRecognition.interimResults = true;
  loungeVoiceRecognition.continuous = false;
  loungeVoiceRecognition.maxAlternatives = 1;

  loungeVoiceRecognition.onstart = () => {
    loungeVoiceActive = true;
    loungeVoiceDraft = "";
    loungeVoicePrefix = loungeMessageInput ? loungeMessageInput.value.trim() : "";
    setLoungeVoiceButtonState(true);
    updateLoungeVoiceStatus("Listening for your lounge message...");
  };

  loungeVoiceRecognition.onresult = (event) => {
    const transcript = Array.from(event.results)
      .map((result) => (result[0] && result[0].transcript ? result[0].transcript : ""))
      .join(" ")
      .trim();
    loungeVoiceDraft = transcript;
    if (loungeMessageInput) {
      const combined = [loungeVoicePrefix, transcript].filter(Boolean).join(" ").trim();
      loungeMessageInput.value = combined;
    }
    updateLoungeVoiceStatus(transcript ? `Heard: ${transcript}` : "Listening for your lounge message...");
  };

  loungeVoiceRecognition.onerror = (event) => {
    loungeVoiceActive = false;
    setLoungeVoiceButtonState(false);
    const errorType = event && event.error ? event.error : "unknown issue";
    updateLoungeVoiceStatus(`Voice messages paused: ${errorType}.`);
  };

  loungeVoiceRecognition.onend = () => {
    loungeVoiceActive = false;
    setLoungeVoiceButtonState(false);
    const transcript = [loungeVoicePrefix, loungeVoiceDraft].filter(Boolean).join(" ").trim();
    loungeVoicePrefix = "";
    loungeVoiceDraft = "";
    if (transcript) {
      if (loungeMessageInput) {
        loungeMessageInput.value = transcript;
      }
      updateLoungeVoiceStatus("Voice message captured. Sending it to the lounge...");
      if (loungeForm) {
        loungeForm.requestSubmit();
      }
    } else {
      updateLoungeVoiceStatus("No voice message captured. Try again when you are ready.");
    }
  };

  setLoungeVoiceButtonState(false);
  updateLoungeVoiceStatus("Press Voice message to dictate into the lounge.");
}

function toggleLoungeVoiceInput() {
  if (!LoungeSpeechRecognition || !loungeVoiceRecognition) {
    return;
  }
  if (loungeVoiceActive) {
    stopLoungeVoiceInput();
    return;
  }
  try {
    loungeVoiceRecognition.start();
  } catch (error) {
    updateLoungeVoiceStatus("Voice messages could not start right now. Try again.");
  }
}

  function setAvatarStage(avatar) {
    if (!avatar) {
      return;
    }

  activeAvatar = avatar;
  if (!avatarStageTitle || !avatarStageTagline || !avatarStageStatus || !avatarFace || !avatarMouth || !avatarGlasses || !avatarShoulders || !avatarAppearanceText) {
    updateTutorSummary(activeProfile || {});
    return;
    }
    avatarStageTitle.textContent = avatar.name;
    avatarStageTagline.textContent = avatar.tagline;
    setAvatarStatusText("Ready");
    avatarFace.classList.toggle("portrait-mode", !!avatar.portrait_url);
  avatarShoulders.classList.toggle("hidden", !!avatar.portrait_url);
  if (avatarPortrait) {
    avatarPortrait.src = avatar.portrait_url || "";
    avatarPortrait.alt = `${avatar.name} tutor portrait`;
    avatarPortrait.classList.toggle("hidden", !avatar.portrait_url);
  }
  avatarFace.style.setProperty("--avatar-accent", avatar.accent);
  avatarFace.style.setProperty("--avatar-secondary", avatar.secondary_accent);
  const visuals = (activeProfile && activeProfile.avatar_visuals) || {};
  avatarFace.style.setProperty("--avatar-skin", visuals.skin || "#f4d1b4");
  avatarFace.style.setProperty("--avatar-hair", visuals.hair || "#3b2a22");
  avatarFace.style.setProperty("--avatar-eyes", visuals.eyes || "#2a2017");
  avatarShoulders.style.setProperty("--avatar-outfit", visuals.outfit || avatar.accent);
  avatarShoulders.classList.toggle("hoodie", !!visuals.hoodie);
  avatarGlasses.classList.toggle("hidden", !visuals.glasses);
  avatarAppearanceText.textContent = (activeProfile && activeProfile.appearance_description) || "Friendly, fun, and human-like.";
  updateTutorSummary(activeProfile || {});
  window.dispatchEvent(new CustomEvent("alt:tutor-appearance", { detail: { avatar, visuals } }));
}

function renderWeeklyPreview(plan) {
  if (!weeklyPreviewCards) {
    return;
  }
  weeklyPreviewCards.innerHTML = "";
  if (!plan || plan.message) {
    const emptyCard = document.createElement("div");
    emptyCard.className = "preview-card";
    emptyCard.textContent = (plan && plan.message) || "No weekly preview available yet.";
    weeklyPreviewCards.appendChild(emptyCard);
    return;
  }

  plan.days.slice(0, 3).forEach((day) => {
    const card = document.createElement("div");
    card.className = "preview-card";

    const dayRow = document.createElement("div");
    dayRow.className = "preview-day";
    dayRow.innerHTML = `<span>${day.date}</span><span>${day.total_hours}h</span>`;

    const focusRow = document.createElement("div");
    focusRow.className = "preview-focus";
    day.tasks.slice(0, 4).forEach((task) => {
      const pill = document.createElement("span");
      pill.className = "focus-pill";
      const topic = task.topic || task.subject;
      pill.textContent = `${task.exam} ${task.subject} - ${topic}`;
      focusRow.appendChild(pill);
    });

    card.appendChild(dayRow);
    card.appendChild(focusRow);
    weeklyPreviewCards.appendChild(card);
  });
}

function renderSectionProgress(items) {
  const targets = [sectionProgressList, planSubjectBreakdownList].filter(Boolean);
  if (!targets.length) {
    return;
  }

  targets.forEach((target) => {
    target.innerHTML = "";
  });
  if (!items || !items.length) {
    targets.forEach((target) => {
      const empty = document.createElement("p");
      empty.className = "muted";
      empty.textContent = "No subject data yet.";
      target.appendChild(empty);
    });
    return;
  }

  targets.forEach((target) => {
    items.forEach((item) => {
      const card = document.createElement("div");
      card.className = "section-progress-item";

      const title = document.createElement("p");
      title.className = "exam-chip-title";
      title.textContent = item.subject;

      const stats = document.createElement("div");
      stats.className = "subject-insight-stats";

      const mockStat = document.createElement("span");
      const mockCount = Number(item.mock_tests_taken || 0);
      mockStat.textContent = `${mockCount} mock ${mockCount === 1 ? "test" : "tests"}`;

      const backlogStat = document.createElement("span");
      const backlogHours = Math.round(Number(item.backlog_hours || 0));
      backlogStat.textContent = `~${backlogHours} hrs backlog`;

      const summary = document.createElement("p");
      summary.className = "subject-insight-copy";
      summary.textContent = item.summary || `Not much is logged for ${item.subject} yet.`;

      stats.appendChild(mockStat);
      stats.appendChild(backlogStat);
      card.appendChild(title);
      card.appendChild(stats);
      card.appendChild(summary);
      target.appendChild(card);
    });
  });
}

function renderWeeklyStrategy(plan) {
  if (!weeklyStrategyList) {
    return;
  }

  weeklyStrategyList.innerHTML = "";
  if (!plan || plan.message) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = (plan && plan.message) || "Your weekly strategy notes will appear here.";
    weeklyStrategyList.appendChild(empty);
    return;
  }

  const plannerLens = document.createElement("div");
  plannerLens.className = "weekly-strategy-chip-row";

  const plannerTitle = document.createElement("p");
  plannerTitle.className = "memory-heading";
  plannerTitle.textContent = "Planner lens";
  plannerLens.appendChild(plannerTitle);

  const plannerChips = [
    `Bias: ${String(plan.planner_bias_label || "balanced").replace(/_/g, " ")}`,
    `Practice blocks: ${plan.weekly_test_blocks || 4}`,
  ];
  if (plan.task_learning_notes && plan.task_learning_notes.length) {
    plannerChips.push(plan.task_learning_notes[0]);
  } else if (plan.notes && plan.notes.length) {
    plannerChips.push(plan.notes[0]);
  }

  plannerChips.forEach((item) => {
    const chip = document.createElement("span");
    chip.className = "focus-pill";
    chip.textContent = item;
    plannerLens.appendChild(chip);
  });

  weeklyStrategyList.appendChild(plannerLens);

  if (plan.task_learning_notes && plan.task_learning_notes.length) {
    const taskNotes = document.createElement("div");
    taskNotes.className = "weekly-strategy-item";

    const taskTitle = document.createElement("p");
    taskTitle.className = "exam-chip-title";
    taskTitle.textContent = "Task learning notes";
    taskNotes.appendChild(taskTitle);

    plan.task_learning_notes.slice(0, 4).forEach((item) => {
      const detail = document.createElement("p");
      detail.className = "muted";
      detail.textContent = item;
      taskNotes.appendChild(detail);
    });

    weeklyStrategyList.appendChild(taskNotes);
  }

  if (plan.task_learning_context) {
    const taskContext = document.createElement("div");
    taskContext.className = "weekly-strategy-item";

    const contextTitle = document.createElement("p");
    contextTitle.className = "exam-chip-title";
    contextTitle.textContent = "Mode learning context";
    taskContext.appendChild(contextTitle);

    plan.task_learning_context.split(/\n+/).slice(0, 6).forEach((line) => {
      const detail = document.createElement("p");
      detail.className = "muted";
      detail.textContent = line;
      taskContext.appendChild(detail);
    });

    weeklyStrategyList.appendChild(taskContext);
  }

  const strongest = document.createElement("div");
  strongest.className = "weekly-strategy-chip-row";
  const strongestTitle = document.createElement("p");
  strongestTitle.className = "memory-heading";
  strongestTitle.textContent = "Strong areas to maintain";
  strongest.appendChild(strongestTitle);
  ((plan.strongest_sections && plan.strongest_sections.length ? plan.strongest_sections : ["Still being established"]) || []).forEach((item) => {
    const chip = document.createElement("span");
    chip.className = "focus-pill strength-pill";
    chip.textContent = item;
    strongest.appendChild(chip);
  });

  const weakest = document.createElement("div");
  weakest.className = "weekly-strategy-chip-row";
  const weakestTitle = document.createElement("p");
  weakestTitle.className = "memory-heading";
  weakestTitle.textContent = "Weak areas to attack";
  weakest.appendChild(weakestTitle);
  ((plan.weakest_sections && plan.weakest_sections.length ? plan.weakest_sections : ["No clear weak section yet"]) || []).forEach((item) => {
    const chip = document.createElement("span");
    chip.className = "focus-pill warning-pill";
    chip.textContent = item;
    weakest.appendChild(chip);
  });

  weeklyStrategyList.appendChild(strongest);
  weeklyStrategyList.appendChild(weakest);

  if (plan.jee_track_mode && plan.jee_track_mode !== "not_jee") {
    const trackRow = document.createElement("div");
    trackRow.className = "weekly-strategy-chip-row";

    const trackTitle = document.createElement("p");
    trackTitle.className = "memory-heading";
    trackTitle.textContent = "JEE track";
    trackRow.appendChild(trackTitle);

    const trackChip = document.createElement("span");
    trackChip.className = "focus-pill";
    trackChip.textContent = String(plan.jee_track_mode).replace(/_/g, " ");
    trackRow.appendChild(trackChip);

    weeklyStrategyList.appendChild(trackRow);
  }

  if (plan.practice_rules && plan.practice_rules.length) {
    const practiceRow = document.createElement("div");
    practiceRow.className = "weekly-strategy-chip-row";

    const practiceTitle = document.createElement("p");
    practiceTitle.className = "memory-heading";
    practiceTitle.textContent = "Weekly rules";
    practiceRow.appendChild(practiceTitle);

    plan.practice_rules.forEach((item) => {
      const chip = document.createElement("span");
      chip.className = "focus-pill";
      chip.textContent = item;
      practiceRow.appendChild(chip);
    });

    weeklyStrategyList.appendChild(practiceRow);
  }

  (plan.weekly_strategy || []).forEach((item) => {
    const card = document.createElement("div");
    card.className = "weekly-strategy-item";

    const title = document.createElement("p");
    title.className = "exam-chip-title";
    title.textContent = item.title;

    const detail = document.createElement("p");
    detail.className = "muted";
    detail.textContent = item.detail;

    card.appendChild(title);
    card.appendChild(detail);
    weeklyStrategyList.appendChild(card);
  });

  if (plan.strategy_sources && plan.strategy_sources.length) {
    const sourcesRow = document.createElement("div");
    sourcesRow.className = "weekly-strategy-chip-row";

    const sourceTitle = document.createElement("p");
    sourceTitle.className = "memory-heading";
    sourceTitle.textContent = "Trusted source blend";
    sourcesRow.appendChild(sourceTitle);

    plan.strategy_sources.forEach((item) => {
      const chip = document.createElement("a");
      chip.className = "source-chip";
      chip.href = item.url || "#";
      chip.target = "_blank";
      chip.rel = "noreferrer";
      chip.textContent = item.label || "Learning source";
      sourcesRow.appendChild(chip);
    });

    weeklyStrategyList.appendChild(sourcesRow);
  }
}

function updateOverviewSnapshotStripFromWeeklyPlan(plan) {
  if (!overviewTodayText || !overviewWeekText || !overviewNextText) {
    return;
  }

  if (!plan || plan.message) {
    overviewTodayText.textContent = "Steady start";
    overviewWeekText.textContent = "-";
    overviewNextText.textContent = "Open your weekly plan";
    return;
  }

  const todayTask = (plan.days && plan.days[0] && plan.days[0].tasks && plan.days[0].tasks[0]) || null;
  overviewTodayText.textContent = todayTask
    ? `${todayTask.exam} ${todayTask.subject}`
    : "Steady start";
  overviewWeekText.textContent = `${plan.weekly_scheduled_hours}h planned | ${plan.weekly_test_blocks || 4} practice blocks | ${String(plan.planner_bias_label || "balanced").replace(/_/g, " ")}`;
  overviewNextText.textContent = (plan.weekly_strategy && plan.weekly_strategy[0] && plan.weekly_strategy[0].title)
    || (plan.notes && plan.notes[0])
    || "Open the weekly plan";
}

function renderWeeklyPlan(plan) {
  journeyWeeklySnapshot = plan || null;
  if (weeklyPlanTableBody) {
    weeklyPlanTableBody.innerHTML = "";
  }
  const hasWeeklySummary = weeklyCoreHours && weeklyScheduledHours && weeklyFocusSplit;
  if (!plan || plan.message) {
    if (hasWeeklySummary) {
      weeklyCoreHours.textContent = "-";
      weeklyScheduledHours.textContent = "-";
      weeklyFocusSplit.textContent = "-";
    }
    updateOverviewSnapshotStripFromWeeklyPlan(plan);
    renderSectionProgress([]);
    renderWeeklyStrategy(plan);
    renderWeeklyPreview(plan);
    updateOverviewCommandCenter();
    updateContextPanel(document.querySelector(".tab-panel.active")?.id || "");

    const row = document.createElement("tr");
    const cell = document.createElement("td");
    cell.colSpan = 5;
    cell.textContent = (plan && plan.message) || "No weekly plan available yet.";
    row.appendChild(cell);
    weeklyPlanTableBody.appendChild(row);
    if (plan && plan.mock_notice) {
      const noticeRow = document.createElement("tr");
      const noticeCell = document.createElement("td");
      noticeCell.colSpan = 5;
      noticeCell.className = "muted";
      noticeCell.textContent = plan.mock_notice;
      noticeRow.appendChild(noticeCell);
      weeklyPlanTableBody.appendChild(noticeRow);
    }
    return;
  }

  if (hasWeeklySummary) {
    weeklyCoreHours.textContent = `${plan.weekly_core_hours}h`;
    weeklyScheduledHours.textContent = `${plan.weekly_scheduled_hours}h`;
    weeklyFocusSplit.textContent = plan.exam_totals.map((item) => `${item.exam} ${item.hours}h`).join(" | ");
  }
  updateOverviewSnapshotStripFromWeeklyPlan(plan);
  renderSectionProgress(plan.section_progress || []);
  renderWeeklyStrategy(plan);
  renderWeeklyPreview(plan);
  updateOverviewCommandCenter();
  updateContextPanel(document.querySelector(".tab-panel.active")?.id || "");

  plan.days.forEach((day) => {
    const row = document.createElement("tr");
    row.innerHTML = `<td><strong>${day.label || day.date}</strong><div class="weekly-date">${day.date}</div></td><td><strong>${day.theme || "Study day"}</strong><div class="weekly-date">${day.strategy || ""}</div></td><td>${day.main_focus || "-"}</td><td></td><td><strong>${day.total_hours}h</strong></td>`;
    const focusCell = row.querySelectorAll("td")[3];
    day.tasks.forEach((task) => {
      const pill = document.createElement("span");
      pill.className = "focus-pill";
      const topic = task.topic || task.subject;
      const revisionTopic = task.revision_topic ? `, revise ${task.revision_topic}` : "";
      pill.textContent = `${task.exam} ${task.subject} | ${topic}${revisionTopic} | ${task.session_type || "study"} | ${task.hours}h`;
      focusCell.appendChild(pill);
    });
    weeklyPlanTableBody.appendChild(row);
  });

  if (plan.mock_notice) {
    const noticeRow = document.createElement("tr");
    const noticeCell = document.createElement("td");
    noticeCell.colSpan = 5;
    noticeCell.className = "muted";
    noticeCell.textContent = plan.mock_notice;
    noticeRow.appendChild(noticeCell);
    weeklyPlanTableBody.appendChild(noticeRow);
  }
}

function _toggleJourneyPanels(show) {
  [journeySetupCard, todaysFocusCard, sessionTimerCard, sessionSummaryCard, journeyProgressSidebar, journeyMasteryCard].forEach((panel) => {
    if (!panel) {
      return;
    }
    panel.classList.toggle("hidden", !show);
  });
}

function _formatJourneyHours(value) {
  const hours = Math.max(2, Math.min(10, Number(value || 6)));
  return `${hours} hours/day`;
}

function renderJourneySetup(planSummary = null) {
  if (!journeySetupCard) {
    return;
  }
  const hasJourney = !!(planSummary && (planSummary.topics || planSummary.days || planSummary.first_topic));
  journeySetupCard.classList.toggle("hidden", hasJourney);
  if (journeyHoursLabel) {
    journeyHoursLabel.textContent = _formatJourneyHours(journeyHoursInput ? journeyHoursInput.value : 6);
  }
  if (journeySetupStatus && planSummary && planSummary.message) {
    journeySetupStatus.textContent = planSummary.message;
  }
}

function renderTodaysFocusCard(focus) {
  todaysFocusSnapshot = focus || null;
  const hasFocus = !!(focus && (focus.primary || focus.morning));
  if (!todaysFocusCard) {
    return;
  }
  todaysFocusCard.classList.toggle("hidden", !hasFocus);
  if (!hasFocus) {
    return;
  }
  const morning = focus.primary || focus.morning || {};
  const sessionType = String(morning.session_type || "learn").toUpperCase();
  const subject = String(morning.subject || "").trim() || "Physics";
  const subjectColor = subject.toLowerCase().includes("chem") ? "green" : subject.toLowerCase().includes("math") ? "orange" : "blue";
  todaysSubjectBadge.textContent = subject;
  todaysSubjectBadge.className = `focus-pill subject-${subjectColor}`;
  todaysUnitText.textContent = morning.unit || morning.unit_name || "Unit";
  todaysTopicText.textContent = morning.topic || "Topic";
  todaysSessionBadge.textContent = sessionType;
  todaysConfidenceText.textContent = `Confidence: ${String(focus.confidence_level || morning.confidence_level || "new")}`;
  todaysWeightageText.textContent = `${Number(morning.weightage_percent || morning.jee_weightage_percent || 0)}% of JEE Main`;
  todaysGoalText.textContent = morning.daily_goal || "Daily goal will appear here.";
  todaysFocusSummary.textContent = focus.daily_motivation || "Your session is ready.";
}

function renderJourneyProgressSidebar(planSummary = null, focus = null, masteryMap = null, revisionDue = null) {
  const covered = planSummary && planSummary.topics ? planSummary.topics : [];
  const totalTopics = covered.length || (masteryMap ? Object.keys(masteryMap).length : 0);
  const doneTopics = masteryMap ? Object.values(masteryMap).filter((item) => ["good", "strong"].includes(String(item.confidence_level || "").toLowerCase())).length : 0;
  const currentStreak = activeProfile && activeProfile.current_streak ? activeProfile.current_streak : 0;
  const percent = totalTopics ? Math.round((doneTopics / Math.max(totalTopics, 1)) * 100) : 0;
  if (!journeyProgressSidebar) {
    return;
  }
  journeyProgressSidebar.classList.remove("hidden");
  if (journeyCoveredText) journeyCoveredText.textContent = `Topics covered: ${doneTopics}/${totalTopics || 0}`;
  if (journeyStreakText) journeyStreakText.textContent = `Current streak: ${currentStreak} day(s)`;
  if (journeyOverallText) journeyOverallText.textContent = `Overall journey: ${percent}% complete`;
  const nextMilestone = focus && focus.primary ? `Complete ${focus.primary.unit || focus.primary.unit_name || "today's unit"} in 2 more sessions` : "Complete the next topic in 2 more sessions";
  if (journeyMilestoneText) journeyMilestoneText.textContent = `Next milestone: ${nextMilestone}`;
}

function renderJourneyMasterySummary(masteryMap = null) {
  if (!journeyMasteryCard) {
    return;
  }
  const entries = masteryMap && typeof masteryMap === "object" ? Object.entries(masteryMap) : [];
  const counts = entries.reduce((acc, [, item]) => {
    const label = String(item && item.confidence_level ? item.confidence_level : "new").toLowerCase();
    acc[label] = (acc[label] || 0) + 1;
    return acc;
  }, { new: 0, low: 0, medium: 0, good: 0, strong: 0 });
  const summaryText = entries.length
    ? `New: ${counts.new || 0} - Low: ${counts.low || 0} - Medium: ${counts.medium || 0} - Good: ${counts.good || 0} - Strong: ${counts.strong || 0}`
    : "No mastery data yet. Start a session to build this map.";
  journeyMasteryCard.classList.remove("hidden");
  if (journeyMasterySummary) {
    journeyMasterySummary.textContent = summaryText;
  }
  if (journeyMasteryList) {
    journeyMasteryList.innerHTML = "";
    if (!entries.length) {
      const empty = document.createElement("p");
      empty.className = "muted";
      empty.textContent = "Mastery details will appear after the first few sessions.";
      journeyMasteryList.appendChild(empty);
      return;
    }
    entries.slice(0, 8).forEach(([key, item]) => {
      const row = document.createElement("div");
      row.className = "weekly-strategy-item";
      row.classList.add("chapter-mastery-row");
      const title = document.createElement("strong");
      title.textContent = item.topic || key.replace("::", " - ");
      const meta = document.createElement("p");
      meta.className = "muted";
      const score = item.best_score !== undefined ? `${Math.round(Number(item.best_score) || 0)}%` : "n/a";
      const studied = item.times_studied !== undefined ? item.times_studied : 0;
      meta.textContent = `Confidence: ${item.confidence_level || "new"} - Best score: ${score} - Studied: ${studied} time(s)`;
      const actions = document.createElement("div");
      actions.className = "chapter-mastery-actions";
      if (String(item.status || "not_started").toLowerCase() !== "not_started") {
        const resetBtn = document.createElement("button");
        resetBtn.type = "button";
        resetBtn.className = "ghost-button chapter-reset-btn";
        resetBtn.title = "Restart this chapter from the beginning";
        resetBtn.textContent = "Reset";
        resetBtn.addEventListener("click", (event) => {
          event.stopPropagation();
          resetChapterFromUI({
            unit_name: item.unit_name || item.unit || item.topic || title.textContent,
            subject: item.subject || "",
          });
        });
        actions.appendChild(resetBtn);
      }
      row.append(title, meta, actions);
      journeyMasteryList.appendChild(row);
    });
  }
}

function renderSessionTimer(startedAt = null) {
  journeyTimerStartedAt = startedAt || journeyTimerStartedAt;
  if (!sessionTimerCard) {
    return;
  }
  sessionTimerCard.classList.toggle("hidden", !journeyTimerStartedAt);
  if (journeyTimerInterval) {
    window.clearInterval(journeyTimerInterval);
    journeyTimerInterval = null;
  }
  if (!journeyTimerStartedAt) {
    if (sessionTimerText) sessionTimerText.textContent = "Session timer idle.";
    if (sessionTimerPill) sessionTimerPill.textContent = "00:00";
    return;
  }
  const tick = () => {
    const elapsed = Math.max(0, Math.floor((Date.now() - journeyTimerStartedAt) / 1000));
    const minutes = String(Math.floor(elapsed / 60)).padStart(2, "0");
    const seconds = String(elapsed % 60).padStart(2, "0");
    const text = `${minutes}:${seconds}`;
    if (sessionTimerPill) sessionTimerPill.textContent = text;
    if (sessionTimerText) sessionTimerText.textContent = `Session running for ${text}.`;
  };
  tick();
  journeyTimerInterval = window.setInterval(tick, 1000);
}

function renderSessionSummary(summary = null) {
  if (!sessionSummaryCard) {
    return;
  }
  const show = !!summary;
  sessionSummaryCard.classList.toggle("hidden", !show);
  if (!show) {
    return;
  }
  if (sessionSummaryText) sessionSummaryText.textContent = summary.message || "Session complete.";
  if (sessionSummaryBadge) sessionSummaryBadge.textContent = summary.updated_confidence || "Complete";
  if (sessionScoreText) sessionScoreText.textContent = `Score: ${summary.checkpoint_score !== undefined ? `${summary.checkpoint_score}%` : "-"}`;
  if (sessionNextRevisionText) {
    const revision = (summary.next_revision_dates && summary.next_revision_dates[0]) || "-";
    sessionNextRevisionText.textContent = `Next revision: ${revision}`;
  }
  if (sessionTomorrowText) {
    const nextTopic = summary.next_topic_preview && (summary.next_topic_preview.topic || summary.next_topic_preview.unit || summary.next_topic_preview.unit_name)
      ? (summary.next_topic_preview.topic || summary.next_topic_preview.unit || summary.next_topic_preview.unit_name)
      : "-";
    sessionTomorrowText.textContent = `Tomorrow's topic: ${nextTopic}`;
  }
}

async function refreshJourneyDashboard() {
  if (!activeProfile) {
    return;
  }
  try {
    const response = await fetch(`/api/tutor/todays-session/${encodeURIComponent(activeProfile.name)}`);
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Could not load today's focus.");
    }
    const focus = payload.todays_focus || payload.focus || null;
    const masteryMap = payload.student_state || payload.mastery_map || null;
    todaysFocusSnapshot = focus || null;
    renderTodaysFocusCard(focus);
    renderJourneyProgressSidebar(journeyPlanSnapshot, focus || null, masteryMap, payload.revision_due || []);
    renderJourneyMasterySummary(masteryMap);
    if (focus && focus.primary) {
      _toggleJourneyPanels(true);
      if (journeySetupCard) journeySetupCard.classList.add("hidden");
    } else {
      _toggleJourneyPanels(false);
      if (journeySetupCard) journeySetupCard.classList.remove("hidden");
      renderJourneySetup(null);
    }
  } catch (error) {
    console.warn("Journey dashboard could not refresh:", error);
  }
}

async function setupJourneyFromUI() {
  if (!activeProfile) {
    return;
  }
  const currentStudentId = activeProfile.name;
  const examDate = journeyExamDateInput && journeyExamDateInput.value ? journeyExamDateInput.value : "";
  const hours = Number(journeyHoursInput && journeyHoursInput.value ? journeyHoursInput.value : "6");
  if (!examDate) {
    alert("Please select your exam date before continuing");
    if (journeySetupStatus) journeySetupStatus.textContent = "Please select your exam date before continuing.";
    return;
  }
  const body = {
    student_id: currentStudentId,
    exam_date: examDate,
    hours_per_day: hours,
  };
  console.log("JOURNEY SETUP REQUEST:", body);
  if (journeySetupStatus) journeySetupStatus.textContent = "Mapping your JEE journey...";
  if (setupJourneyBtn) setupJourneyBtn.disabled = true;
  try {
    const response = await fetch("/api/planner/setup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Could not build the journey.");
    }
    journeyPlanSnapshot = payload.plan_summary || null;
    journeyWeeklySnapshot = payload.weekly_plan || null;
    renderJourneySetup(payload.plan_summary || null);
    renderWeeklyPlan(payload.weekly_plan || null);
    renderTodaysFocusCard(payload.todays_focus || null);
    renderJourneyProgressSidebar(payload.plan_summary || null, payload.todays_focus || null, null, payload.todays_focus ? payload.todays_focus.revision_due : []);
    renderJourneyMasterySummary(payload.todays_focus ? payload.todays_focus.student_state : null);
    appendMessage("tutor", "tutor", payload.opening_message || "Your JEE journey is ready.");
    if (journeySetupStatus) journeySetupStatus.textContent = payload.message || "Your journey is ready.";
    if (setupJourneyBtn) setupJourneyBtn.textContent = "Journey ready";
    const focusTopic = payload.todays_focus && payload.todays_focus.primary ? payload.todays_focus.primary.topic : "";
    const focusSubject = payload.todays_focus && payload.todays_focus.primary ? payload.todays_focus.primary.subject : "";
    if (focusTopic) {
      updateAstraCurrentTopic(focusTopic, focusSubject, "weekly_plan");
    }
    await refreshJourneyDashboard();
  } catch (error) {
    if (journeySetupStatus) journeySetupStatus.textContent = error.message;
  } finally {
    if (setupJourneyBtn) setupJourneyBtn.disabled = false;
  }
}

async function startJourneySession() {
  if (!activeProfile) {
    return;
  }
  try {
    const focusPreview = todaysFocusSnapshot && (todaysFocusSnapshot.primary || todaysFocusSnapshot.morning)
      ? (todaysFocusSnapshot.primary || todaysFocusSnapshot.morning)
      : null;
    setAstraStatus(
      focusPreview
        ? `Astra is ready. Today's focus: ${focusPreview.topic || "today's topic"} - ${focusPreview.subject || "study"}`
        : "Astra is ready. Preparing today's focus...",
      "idle"
    );
    logSessionActivity(`Started ${focusPreview && focusPreview.topic ? focusPreview.topic : "today's session"}`);
    const response = await fetch(`/api/tutor/todays-session/${encodeURIComponent(activeProfile.name)}`);
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Could not start today's session.");
    }
    if (todaysFocusCard) {
      todaysFocusCard.classList.add("pulse-focus");
    }
    const morningTopic = payload.todays_focus && payload.todays_focus.primary ? payload.todays_focus.primary.topic : "";
    const morningSubject = payload.todays_focus && payload.todays_focus.primary ? payload.todays_focus.primary.subject : "";
    if (morningTopic) {
      updateAstraCurrentTopic(morningTopic, morningSubject, "weekly_plan");
    }
    sessionCheckpointStats = {
      answered: 0,
      average: 0,
      confidence: (payload.student_state && payload.student_state.confidence_level) || "new",
      topic: morningTopic || "Today",
    };
    appendMessage("tutor", "tutor", payload.opening_message || "Let's begin your session.");
    renderJourneyProgressSidebar(journeyPlanSnapshot || null, payload.todays_focus || null, payload.student_state || null, payload.revision_due || []);
    renderSessionTimer(Date.now());
    renderSessionStats(morningTopic || "Today", sessionCheckpointStats.confidence, Number((payload.student_state && payload.student_state.confidence_level_score) || 0));
    setTimeout(() => {
      if (todaysFocusCard) {
        todaysFocusCard.classList.remove("pulse-focus");
      }
    }, 1200);
    activeJourneySession = payload;
    setAstraStatus(
      morningTopic
        ? `Astra is explaining ${morningTopic}...`
        : "Astra is explaining today's topic...",
      "working"
    );
    setActiveTab("tutorTab");
  } catch (error) {
    appendMessage("tutor", "tutor", `I could not start the session right now: ${error.message}`);
    setAstraStatus(`Could not start the session: ${error.message}`, "warning", true);
  }
}

async function completeJourneySessionFromCheckpoint(checkpointScore) {
  if (!activeProfile || !todaysFocusSnapshot) {
    return;
  }
  const morning = todaysFocusSnapshot.primary || todaysFocusSnapshot.morning || {};
  try {
    setAstraStatus(
      `Updating your progress... ${morning.topic || "current topic"} confidence: ${(checkpointScore >= 85 ? "strong" : checkpointScore >= 70 ? "good" : checkpointScore >= 50 ? "medium" : "low")}`,
      "working"
    );
    const response = await fetch("/api/tutor/complete-session", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        student_id: activeProfile.name,
        topic: morning.topic || "",
        subject: morning.subject || "",
        unit_name: morning.unit || morning.unit_name || "",
        checkpoint_score: checkpointScore,
        duration_minutes: journeyTimerStartedAt ? Math.max(1, Math.round((Date.now() - journeyTimerStartedAt) / 60000)) : 0,
        session_type: morning.session_type || "learn",
        understood: checkpointScore >= 60,
      }),
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Could not complete the session.");
    }
    const nextTopic = payload.next_topic_preview || {};
    if (nextTopic.topic) {
      updateAstraCurrentTopic(nextTopic.topic, nextTopic.subject || "", "weekly_plan");
    }
    activeJourneySession = null;
    renderSessionTimer(null);
    renderSessionSummary({
      ...payload,
      message: payload.encouragement_message || "Great work.",
      checkpoint_score: checkpointScore,
    });
    renderJourneyProgressSidebar(journeyPlanSnapshot, payload.next_topic_preview || null, payload.result || null, payload.result ? payload.result.next_revision_dates || [] : []);
    const nextRevision = payload.result && payload.result.next_revision_dates && payload.result.next_revision_dates.length ? payload.result.next_revision_dates[0] : null;
    const nextRevisionDate = nextRevision ? new Date(nextRevision) : null;
    const nextRevisionDays = nextRevisionDate && !Number.isNaN(nextRevisionDate.getTime())
      ? Math.max(1, Math.round((nextRevisionDate.getTime() - Date.now()) / 86400000))
      : null;
    showToast(`Plan updated - ${morning.topic || "topic"} marked as ${(payload.result && payload.result.confidence_level) || "updated"}. Next revision in ${nextRevisionDays || "a few"} days.`);
    await refreshEngagementAfterLPAward(payload.lp_awards);
    logSessionActivity(`Checkpoint completed for ${morning.topic || "current topic"}: ${checkpointScore}%`);
    renderSessionStats(morning.topic || "Today", (payload.result && payload.result.confidence_level) || "updated", checkpointScore);
    if (payload.weekly_plan_updated) {
      await refreshWeeklyPlan();
    }
    await refreshJourneyDashboard();
    await refreshTodayPhaseAndBacklog();
    setAstraStatus(
      payload.next_topic_preview && payload.next_topic_preview.topic
        ? `Plan updated. Next up: ${payload.next_topic_preview.topic}`
        : "Plan updated.",
      "success",
      true
    );
  } catch (error) {
    console.warn("Could not complete journey session:", error);
    setAstraStatus(`Could not update plan: ${error.message}`, "warning", true);
  }
}

function renderAvatars(selectedAvatarId) {
  if (!avatarGrid) {
    return;
  }
  avatarGrid.innerHTML = "";
  avatarPresets.forEach((avatar) => {
    const card = document.createElement("button");
    card.type = "button";
    card.className = `avatar-card ${selectedAvatarId === avatar.id ? "active" : ""}`;

    const portrait = document.createElement("img");
    portrait.className = "avatar-card-portrait";
    portrait.src = getTutorPersonalityPortrait(avatar);
    portrait.alt = `${avatar.name} portrait`;
    portrait.loading = "eager";
    portrait.decoding = "async";
    card.appendChild(portrait);

    const accent = document.createElement("div");
    accent.className = "avatar-accent";
    accent.style.background = `linear-gradient(145deg, ${avatar.accent}, ${avatar.secondary_accent})`;

    const title = document.createElement("h3");
    title.textContent = avatar.name;

    const tagline = document.createElement("p");
    tagline.className = "muted";
    tagline.textContent = avatar.tagline;

    card.appendChild(accent);
    card.appendChild(title);
    card.appendChild(tagline);
    card.addEventListener("click", () => selectAvatar(avatar.id));
    avatarGrid.appendChild(card);
  });
}

function getTutorPersonalityPortrait(avatar) {
  if (!avatar) {
    return "/media/tutor-faces/GeniusStrategistGuideFemaleMain1.png";
  }
  if (avatar.portrait_url) {
    return avatar.portrait_url;
  }
  if (avatar.id === "friendly-senior") {
    return "/media/tutor-faces/EnergeticGuideFemaleMain1.png";
  }
  return "/media/tutor-faces/GeniusStrategistGuideFemaleMain1.png";
}

function renderHomeTutorPersonalityGrid() {
  if (!homeTutorPersonalityGrid) {
    return;
  }

  homeTutorPersonalityGrid.innerHTML = "";
  const selectedAvatarId = activeProfile?.selected_avatar || activeAvatar?.id || "";
  const avatars = avatarPresets.length ? avatarPresets : [];

  if (!avatars.length) {
    const emptyState = document.createElement("p");
    emptyState.className = "muted";
    emptyState.textContent = "Tutor personalities will appear here once the avatar profiles are ready.";
    homeTutorPersonalityGrid.appendChild(emptyState);
    return;
  }

  avatars.forEach((avatar) => {
    const card = document.createElement("article");
    card.className = `home-tutor-card ${selectedAvatarId === avatar.id ? "selected" : ""}`;

    const portrait = document.createElement("img");
    portrait.className = "home-tutor-card-image";
    portrait.src = getTutorPersonalityPortrait(avatar);
    portrait.alt = `${avatar.name} face`;
    portrait.loading = "lazy";
    portrait.decoding = "async";

    const body = document.createElement("div");
    body.className = "home-tutor-card-body";

    const name = document.createElement("h3");
    name.className = "home-tutor-card-title";
    name.textContent = avatar.name;

    const description = document.createElement("p");
    description.className = "home-tutor-card-description";
    description.textContent = `${avatar.tagline} ${avatar.sample_line || ""}`.trim();

    const button = document.createElement("button");
    button.type = "button";
    button.className = "home-tutor-select-btn";
    button.textContent = "Select this tutor";
    button.addEventListener("click", (event) => {
      event.stopPropagation();
      selectAvatar(avatar.id);
    });

    body.appendChild(name);
    body.appendChild(description);
    body.appendChild(button);
    card.appendChild(portrait);
    card.appendChild(body);
    homeTutorPersonalityGrid.appendChild(card);
  });
}

function supportsSpeech() {
  return "speechSynthesis" in window && "SpeechSynthesisUtterance" in window;
}

function loadBrowserVoices() {
  if (supportsSpeech()) {
    browserVoices = window.speechSynthesis.getVoices();
  }
}

function findVoiceForAvatar(avatar) {
  if (!avatar || !browserVoices.length) {
    return null;
  }

  const keywords = avatar.voice_keywords || [];
  for (const keyword of keywords) {
    const match = browserVoices.find((voice) => voice.name.toLowerCase().includes(keyword));
    if (match) {
      return match;
    }
  }

  const languagePrefix = getLanguagePrefix(currentLanguage);
  return browserVoices.find((voice) => voice.lang.toLowerCase().startsWith(languagePrefix))
    || browserVoices.find((voice) => voice.lang.toLowerCase().startsWith("en"))
    || browserVoices[0]
    || null;
}

function getFemaleTutorAvatar() {
  const femaleAvatar = avatarPresets.find((avatar) => ["calm-mentor", "friendly-senior"].includes(avatar.id));
  return femaleAvatar || avatarPresets[0] || activeAvatar || null;
}

function getSpeechAvatarForMode(mode = "tutor") {
  if (mode === "tutor") {
    return getFemaleTutorAvatar();
  }
  return activeAvatar || avatarPresets[0] || getFemaleTutorAvatar();
}

function ensureTutorRoomPersona() {
  const femaleAvatar = getFemaleTutorAvatar();
  if (femaleAvatar && (!activeAvatar || activeAvatar.id !== femaleAvatar.id)) {
    setAvatarStage(femaleAvatar);
  }
}

function updateTalkingFace(step = 0) {
  if (!avatarFace || !avatarMouth) {
    return;
  }
  avatarFace.classList.add("speaking");
  avatarMouth.className = "mouth";
  avatarMouth.classList.add(`open-${step}`);
}

function stopTalkingFace() {
  if (!avatarFace || !avatarMouth) {
    return;
  }
  avatarFace.classList.remove("speaking");
  avatarMouth.className = "mouth";
}

  function speakText(text) {
    if (!supportsSpeech() || !text) {
      return;
    }

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
  const currentMode = getActiveConversationModeFromUI();
  const avatar = getSpeechAvatarForMode(currentMode) || activeAvatar || avatarPresets[0] || null;
  const chosenVoice = findVoiceForAvatar(avatar);

  if (chosenVoice) {
    utterance.voice = chosenVoice;
  }
    const pacingMode = responsePacingSelect ? responsePacingSelect.value : "standard";
    const pacingScale = pacingMode === "slow" ? 0.86 : pacingMode === "gentle" ? 0.93 : 1;
    utterance.rate = ((avatar && avatar.voice_rate) || 0.96) * pacingScale;
    utterance.pitch = (avatar && avatar.voice_pitch) || 1.0;
    setCaption(text);
    const videoTutorActive = document.querySelector(".tab-panel.active")?.id === "videoTutorTab";
    if (avatarRenderer && videoTutorActive) {
      avatarRenderer.startSpeakingAnimation();
    }
    setAvatarStatusText("Speaking");
    updateTalkingFace(1);
    activeSpeechUtterance = utterance;

  utterance.onboundary = (event) => {
    if (typeof event.charIndex === "number") {
      updateTalkingFace((Math.floor(event.charIndex / 5) % 3) + 1);
      if (autoCaptionMode.checked) {
        const nextCaption = text.slice(event.charIndex, Math.min(text.length, event.charIndex + 160)).trim();
        if (nextCaption) {
          setCaption(nextCaption);
        }
      }
    }
  };

    utterance.onend = () => {
      if (avatarRenderer && videoTutorActive) {
        avatarRenderer.stopSpeakingAnimation();
        avatarRenderer.playNodGesture();
      }
      setAvatarStatusText("Ready");
      stopTalkingFace();
      if (activeSpeechUtterance === utterance) {
        activeSpeechUtterance = null;
      }
    if (autoCaptionMode.checked) {
      setCaption(text);
    }
    updateTutorRoomLivePanel();
  };

    utterance.onerror = () => {
      if (avatarRenderer && videoTutorActive) {
        avatarRenderer.stopSpeakingAnimation();
      }
      setAvatarStatusText("Ready");
      stopTalkingFace();
      if (activeSpeechUtterance === utterance) {
        activeSpeechUtterance = null;
      }
    updateTutorRoomLivePanel();
  };

  window.speechSynthesis.speak(utterance);
  updateTutorRoomLivePanel();
}

  function pauseSpeaking() {
    if (!supportsSpeech()) {
      return;
    }
    if (window.speechSynthesis.speaking && !window.speechSynthesis.paused) {
      window.speechSynthesis.pause();
      setAvatarStatusText("Voice Paused");
      setCaption("Speech paused.");
    }
  }

  function resumeSpeaking() {
    if (!supportsSpeech()) {
      return;
    }
    if (window.speechSynthesis.paused) {
      window.speechSynthesis.resume();
      setAvatarStatusText("Speaking");
      setCaption("Speech resumed.");
    }
  }

  function stopSpeaking() {
    if (!supportsSpeech()) {
      updateTutorRoomLivePanel();
      return;
    }
    window.speechSynthesis.cancel();
    activeSpeechUtterance = null;
    if (avatarRenderer) {
      avatarRenderer.stopSpeakingAnimation();
    }
    setAvatarStatusText("Ready");
    stopTalkingFace();
    setCaption("Speech stopped.");
    updateTutorRoomLivePanel();
  }

function pauseTutorNarration() {
  if (activeTutorNarration) {
    activeTutorNarration.paused = true;
    if (!activeTutorNarration.checkpoint) {
      activeTutorNarration.checkpoint = activeTutorNarration.text || "";
    }
  }
  pauseSpeaking();
  updateTutorRoomLivePanel();
}

function resumeTutorNarration() {
  if (activeTutorNarration) {
    activeTutorNarration.paused = false;
    if (activeTutorNarration.mode === "tutor" && autoCaptionMode.checked) {
      setCaption(activeTutorNarration.output || activeTutorNarration.text || "Resuming reply...");
    }
  }
  resumeSpeaking();
  updateTutorRoomLivePanel();
}

function saveTutorCheckpoint(mode, sourceText, replyText) {
  const normalizedMode = mode || "tutor";
  tutorReplyCheckpoints[normalizedMode] = {
    mode: normalizedMode,
    source_text: sourceText || "",
    reply_text: replyText || "",
    created_at: new Date().toISOString(),
  };
}

function interruptTutorOutput(mode) {
  const activeMode = mode || (activeTutorNarration && activeTutorNarration.mode) || "tutor";
  if (activeTutorNarration && activeTutorNarration.mode === activeMode) {
    saveTutorCheckpoint(activeMode, activeTutorNarration.text, activeTutorNarration.output || activeTutorNarration.text);
    pauseTutorNarration();
    updateTutorRoomLivePanel();
    return;
  }
  if (lastRepliesByMode[activeMode] || lastTutorReply) {
    saveTutorCheckpoint(activeMode, "", lastRepliesByMode[activeMode] || lastTutorReply);
  }
  pauseSpeaking();
  updateTutorRoomLivePanel();
}

async function resumeTutorCheckpoint(mode = "tutor") {
  const checkpoint = tutorReplyCheckpoints[mode];
  if (activeTutorNarration && activeTutorNarration.mode === mode && activeTutorNarration.paused) {
    resumeTutorNarration();
    return true;
  }
  if (!activeProfile || !checkpoint || !checkpoint.reply_text) {
    return false;
  }
  const continuationPrompt = checkpoint.source_text
    ? `Continue from the last checkpoint without repeating the earlier parts. The student interrupted the explanation, so resume naturally from here: ${checkpoint.reply_text}`
    : `Continue from the last checkpoint without repeating the earlier parts. Resume naturally from this prior answer: ${checkpoint.reply_text}`;
  await sendMessage(continuationPrompt);
  return true;
}

function getActiveConversationModeFromUI() {
  const activeTabElement = document.querySelector(".tab-panel.active");
  const activeTab = activeTabElement ? activeTabElement.id : "tutorTab";
  return activeTab === "guideTab"
    ? "guide"
    : activeTab === "loungeTab"
    ? "lounge"
    : activeTab === "practiceTab"
    ? "practice"
    : activeTab === "lastMinuteTab"
    ? "last_minute"
    : activeTab === "tipsTab"
    ? "tips"
    : "tutor";
}

function renderTabManager() {
  if (!tabManager) {
    return;
  }

  tabManager.innerHTML = "";
  getVisibleTabOrder().forEach((key, index, visibleOrder) => {
    const row = document.createElement("div");
    row.className = "tab-manager-row";

    const label = document.createElement("span");
    label.textContent = TAB_CONFIG[key].label;

    const controls = document.createElement("div");
    controls.className = "tab-manager-controls";

    const leftButton = document.createElement("button");
    leftButton.type = "button";
    leftButton.className = "ghost-button mini-button";
    leftButton.textContent = "Left";
    leftButton.disabled = index === 0;
    leftButton.addEventListener("click", () => moveTab(key, -1));

    const rightButton = document.createElement("button");
    rightButton.type = "button";
    rightButton.className = "ghost-button mini-button";
    rightButton.textContent = "Right";
    rightButton.disabled = index === visibleOrder.length - 1;
    rightButton.addEventListener("click", () => moveTab(key, 1));

    controls.appendChild(leftButton);
    controls.appendChild(rightButton);
    row.appendChild(label);
    row.appendChild(controls);
    tabManager.appendChild(row);
  });
}

function applyTabOrder() {
  currentTabOrder.forEach((key) => {
    const config = TAB_CONFIG[key];
    const button = tabBar.querySelector(`[data-tab-key="${key}"]`);
    const panel = document.getElementById(config.buttonTab);
    const groupContainer = button ? tabBar.querySelector(`[data-nav-group-container="${button.dataset.navGroup || "home"}"] .nav-hub-buttons`) : null;
    if (button) {
      if (groupContainer) {
        groupContainer.appendChild(button);
      } else {
        tabBar.appendChild(button);
      }
    }
    if (panel) {
      panel.parentElement.appendChild(panel);
    }
  });
  localStorage.setItem("alt_tab_order", JSON.stringify(currentTabOrder));
  const activePanelId = document.querySelector(".tab-panel.active")?.id || "overviewTab";
  keepTabPanelNearTop(activePanelId);
  refreshTabCollections();
  renderTabManager();
  applyLeagueVisibility();
}

function moveTab(key, direction) {
  const index = currentTabOrder.indexOf(key);
  const nextIndex = index + direction;
  if (index < 0 || nextIndex < 0 || nextIndex >= currentTabOrder.length) {
    return;
  }
  const nextOrder = [...currentTabOrder];
  [nextOrder[index], nextOrder[nextIndex]] = [nextOrder[nextIndex], nextOrder[index]];
  currentTabOrder = nextOrder;
  applyTabOrder();
}

async function fetchAvatarPresets() {
  const response = await fetch("/api/avatar-presets");
  const payload = await response.json();
  avatarPresets = payload.avatars || [];
}

async function fetchExamCatalog() {
  const response = await fetch("/api/exam-catalog");
  const payload = await response.json();
  examCatalog = payload.exams || [];
  renderExamCatalogOptions();
}

async function fetchStudyGroups(studentName) {
  if (!studentName) {
    renderStudyGroups(null);
    return;
  }
  const response = await fetch(`/api/group-sessions/matches/${encodeURIComponent(studentName)}`);
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || "Could not load study groups.");
  }
  renderStudyGroups(payload);
}

async function fetchProgress(studentName) {
  try {
    if (!studentName) {
      renderProgressSnapshot(null);
      renderChapterMasteryBoard(null);
      renderChapterAnalytics(null);
      renderChapterRevisionTracker(null);
      return;
    }
    setAstraStatus("Pulling progress and mastery signals...", "working");
    const [progressResponse, masteryResponse, analyticsResponse, summariesResponse] = await Promise.all([
      fetch(`/api/progress/${encodeURIComponent(studentName)}`),
      fetch(`/api/progress/chapter-mastery/${encodeURIComponent(studentName)}`),
      fetch(`/api/progress/analytics/${encodeURIComponent(studentName)}`),
      fetch(`/api/session/chapter-summaries/${encodeURIComponent(studentName)}`),
    ]);
    const [progressPayload, masteryPayload, analyticsPayload, summariesPayload] = await Promise.all([
      progressResponse.json(),
      masteryResponse.json(),
      analyticsResponse.json(),
      summariesResponse.json(),
    ]).catch((error) => {
      throw error;
    });
    if (!progressResponse.ok) {
      throw new Error(progressPayload.detail || "Could not load progress.");
    }
    renderProgressSnapshot(progressPayload);
    renderChapterMasteryBoard(masteryPayload);
    renderChapterAnalytics(analyticsPayload);
    renderChapterRevisionTracker(summariesPayload);
    void loadProgressInsight();
    updateContextPanel("progressTab");
    setAstraStatus("Progress board updated.", "success", true);
  } catch (error) {
    console.warn("Could not load progress:", error);
    setAstraStatus(`Could not load progress: ${error.message}`, "warning", true);
  }
}

async function fetchStudentInsights(studentName) {
  if (!studentName) {
    renderStudentInsights(null);
    return;
  }
  const response = await fetch(`/api/student-insights/${encodeURIComponent(studentName)}`);
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || "Could not load student insights.");
  }
  renderStudentInsights(payload || null);
}

async function summarizeLatestTutorAnswer() {
  if (!activeProfile) {
    return;
  }

  const answerText = (lastRepliesByMode.tutor || lastTutorReply || "").trim();
  if (!answerText) {
    renderSummaryPanel("There is no tutor answer to summarize yet. Ask the tutor something first.");
    setActiveStudioPane("summaryPanel");
    return;
  }

  if (summarizeTutorBtn) {
    summarizeTutorBtn.disabled = true;
  }
  if (quickSummaryBtn) {
    quickSummaryBtn.disabled = true;
  }

  try {
    const response = await fetch("/api/summarize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        student_name: activeProfile.name,
        answer_text: answerText,
        response_language: currentLanguage,
        conversation_mode: "tutor",
      }),
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Could not summarize that answer.");
    }
    renderSummaryPanel(payload.summary || "");
    setActiveStudioPane("summaryPanel");
  } catch (error) {
    renderSummaryPanel(`Could not summarize right now: ${error.message}`);
    setActiveStudioPane("summaryPanel");
  } finally {
    if (summarizeTutorBtn) {
      summarizeTutorBtn.disabled = false;
    }
    if (quickSummaryBtn) {
      quickSummaryBtn.disabled = false;
    }
  }
}

async function saveProgressItem() {
  if (!activeProfile || !progressTopicInput || !saveProgressItemBtn) {
    return;
  }

  const topic = (progressTopicInput && progressTopicInput.value.trim()) || "";
  if (!topic) {
    if (progressReminderText) {
      progressReminderText.textContent = "Add at least a topic or chapter name before saving.";
    }
    return;
  }

  saveProgressItemBtn.disabled = true;
  try {
    const response = await fetch("/api/progress/item", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        student_name: activeProfile.name,
        exam: (progressExamInput && progressExamInput.value.trim()) || "",
        subject: (progressSubjectInput && progressSubjectInput.value.trim()) || "",
        topic,
        status: (progressStatusSelect && progressStatusSelect.value) || "pending",
        note: (progressNoteInput && progressNoteInput.value.trim()) || "",
      }),
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Could not save that progress item.");
    }
    renderProgressSnapshot(payload);
    await fetchStudentInsights(activeProfile.name);
    await refreshEngagementAfterLPAward(payload.lp_awards);
    await fetchVideoLibrary(activeProfile.name);
    progressTopicInput.value = "";
    progressNoteInput.value = "";
    await fetchStorageStatus(activeProfile.name);
    } catch (error) {
    if (progressReminderText) {
      progressReminderText.textContent = error.message;
    }
  } finally {
    saveProgressItemBtn.disabled = false;
  }
}

async function updateProgressItemStatus(itemId, status) {
  if (!activeProfile || !itemId) {
    return;
  }
  try {
    const response = await fetch("/api/progress/status", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        student_name: activeProfile.name,
        item_id: itemId,
        status,
      }),
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Could not update that progress item.");
    }
    renderProgressSnapshot(payload);
    await fetchStudentInsights(activeProfile.name);
    await refreshEngagementAfterLPAward(payload.lp_awards);
    await fetchVideoLibrary(activeProfile.name);
    await fetchStorageStatus(activeProfile.name);
    } catch (error) {
    if (progressReminderText) {
      progressReminderText.textContent = error.message;
    }
  }
}

async function fetchPracticeAnalytics(studentName) {
  if (!studentName) {
    renderPracticeAnalytics(null);
    return;
  }
  const response = await fetch(`/api/analytics/${encodeURIComponent(studentName)}`);
  const payload = await response.json();
  renderPracticeAnalytics(payload);
}

function renderPracticeAnalytics(payload) {
  if (!payload) {
    if (performanceChartSummary) {
      performanceChartSummary.textContent = "Your practice trend will appear here.";
    }
    if (performanceChartBars) {
      performanceChartBars.innerHTML = '<p class="muted">No practice attempts logged yet.</p>';
    }
    return;
  }

  const attempts = Array.isArray(payload.attempts) ? payload.attempts.slice(-7) : [];
  if (performanceChartSummary) {
    const totalAttempts = Number(payload.total_attempts || 0);
    const recentAccuracy = Number(payload.recent_accuracy || payload.average_accuracy || 0);
    const trend = String(payload.trend_signal || "building").replace(/_/g, " ");
    performanceChartSummary.textContent = totalAttempts
      ? `${totalAttempts} practice attempt(s) logged | recent accuracy ${recentAccuracy.toFixed(0)}% | ${trend}`
      : "Your practice trend will appear here.";
  }
  if (!performanceChartBars) {
    return;
  }
  performanceChartBars.innerHTML = "";
  if (!attempts.length) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = "No practice attempts logged yet.";
    performanceChartBars.appendChild(empty);
    return;
  }
  attempts.forEach((attempt) => {
    const row = document.createElement("div");
    row.className = "performance-bar-row";
    const label = document.createElement("span");
    label.className = "performance-bar-label";
    label.textContent = attempt.timestamp ? String(attempt.timestamp).slice(5, 10) : String(attempt.mode || "Practice");
    const track = document.createElement("div");
    track.className = "performance-bar-track";
    const fill = document.createElement("div");
    fill.className = "performance-bar-fill";
    const accuracy = Math.max(0, Math.min(100, Number(attempt.accuracy_percent || 0)));
    fill.style.width = `${Math.max(6, Math.round(accuracy))}%`;
    const value = document.createElement("span");
    value.className = "performance-bar-value";
    value.textContent = `${accuracy.toFixed(0)}%`;
    track.appendChild(fill);
    row.append(label, track, value);
    performanceChartBars.appendChild(row);
  });
}

async function selectAvatar(avatarId) {
  if (!activeProfile) {
    return;
  }

  const response = await fetch("/api/avatar/select", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      student_name: activeProfile.name,
      avatar_id: avatarId,
    }),
  });
  const payload = await response.json();
  if (!response.ok) {
    appendMessage("tutor", "tutor", payload.detail || "Could not select that avatar.");
    return;
  }

    activeProfile = payload.profile;
    setAvatarStage(payload.avatar);
    void initAvatar();
    renderTutorBrain(payload.tutor_brain || buildLocalTutorBrain(activeProfile, payload.avatar, "tutor"));
    renderAvatars(activeProfile.selected_avatar);
    renderHomeTutorPersonalityGrid();
  preferTutorVideosForAvatar(payload.avatar);
  if (studentSubcopy) {
    studentSubcopy.textContent = `Current AI teacher style: ${payload.avatar.name}.`;
  }
  appendMessage("tutor", "tutor", `I will now guide you with the ${payload.avatar.name} persona.`);
  speakText(payload.avatar.sample_line);
}

async function saveTutorName() {
  if (!activeProfile) {
    return;
  }

  const response = await fetch("/api/tutor/customize", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      student_name: activeProfile.name,
      tutor_name: tutorNameInput.value.trim(),
      tutor_personality_preset: tutorPersonaPresetSelect ? tutorPersonaPresetSelect.value : "",
      tutor_personality_traits: selectedTutorTraits,
      tutor_personality_notes: tutorStyleInput.value.trim(),
      tutor_style: buildTutorStyleSummary(),
      appearance_description: tutorAppearanceInput.value.trim(),
    }),
  });
  const payload = await response.json();
  if (!response.ok) {
    appendMessage("tutor", "tutor", payload.detail || "I could not save that tutor setup.");
    return;
  }

  activeProfile = payload.profile;
  tutorNameInput.value = activeProfile.tutor_name || "";
  applyTutorPersonalityToForm(activeProfile);
  tutorAppearanceInput.value = activeProfile.appearance_description || "";
  setAvatarStage(activeAvatar || avatarPresets[0]);
  renderTutorBrain(buildLocalTutorBrain(activeProfile, activeAvatar || avatarPresets[0], "tutor"));
  updateTutorSummary(activeProfile);
  await fetchStudyGroups(activeProfile.name);
  appendMessage("tutor", "tutor", `Perfect. I will show up as ${activeProfile.tutor_name} with the style you described.`);
}

async function joinStudyGroup(group) {
  if (!activeProfile || !group) {
    return;
  }
  const response = await fetch("/api/group-sessions/join", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: activeProfile.name,
      topic: group.topic || "",
      subject: group.subject || "",
      exam: group.exam || "",
      pace_band: group.pace_band || "",
    }),
  });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || "Could not join that study group.");
  }
  renderActiveGroupSession(payload.session || null);
  openGroupSession(payload.session || null);
  await fetchStudyGroups(activeProfile.name);
}

async function sendGroupMainMessage(content, senderType = "student") {
  if (!activeProfile || !activeGroupSession || !activeGroupSession.id) {
    return;
  }
  const response = await fetch(`/api/group-sessions/${encodeURIComponent(activeGroupSession.id)}/main-message`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: activeProfile.name,
      sender_type: senderType,
      content: content || "",
    }),
  });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || "Could not send that group message.");
  }
  activeGroupSession = { ...(payload.session || activeGroupSession), main_messages: payload.main_messages || [] };
  openGroupSession(activeGroupSession, { silent: true });
}

async function stepIntoGroupBreakout() {
  if (!activeProfile || !activeGroupSession || !activeGroupSession.id) {
    return;
  }
  const response = await fetch(`/api/group-sessions/${encodeURIComponent(activeGroupSession.id)}/breakout`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: activeProfile.name }),
  });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || "Could not open breakout.");
  }
  activeGroupSession = { ...(payload.session || activeGroupSession), breakout_messages: payload.breakout_messages || [], current_user_status: "in_breakout" };
  openGroupSession(activeGroupSession, { silent: true });
}

async function sendGroupBreakoutMessage(content) {
  if (!activeProfile || !activeGroupSession || !activeGroupSession.id) {
    return;
  }
  const response = await fetch(`/api/group-sessions/${encodeURIComponent(activeGroupSession.id)}/breakout-message`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: activeProfile.name,
      sender_type: "student",
      content,
    }),
  });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || "Could not send that breakout message.");
  }
  activeGroupSession = { ...(payload.session || activeGroupSession), breakout_messages: payload.breakout_messages || [], current_user_status: "in_breakout" };
  openGroupSession(activeGroupSession, { silent: true });
}

async function rejoinGroupSession() {
  if (!activeProfile || !activeGroupSession || !activeGroupSession.id) {
    return;
  }
  const response = await fetch(`/api/group-sessions/${encodeURIComponent(activeGroupSession.id)}/rejoin`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: activeProfile.name }),
  });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || "Could not rejoin the group session.");
  }
  activeGroupSession = {
    ...(payload.session || activeGroupSession),
    main_messages: payload.main_messages || [],
    breakout_messages: payload.breakout_messages || [],
    current_user_status: "in_main",
  };
  openGroupSession(activeGroupSession, { silent: true });
}
async function saveExamPlans(exams, successMessage) {
  if (!activeProfile) {
    return;
  }

  const response = await fetch("/api/profile/exams", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      student_name: activeProfile.name,
      exams,
    }),
  });
  const payload = await response.json();
  if (!response.ok) {
    appendMessage("tutor", "tutor", payload.detail || "I could not update your exams.");
    return;
  }

  activeProfile = payload.profile;
  renderExamManager(activeProfile.exams || []);
  await refreshWeeklyPlan();
  await fetchLearningSources(activeProfile.name);
  await fetchVideoLibrary(activeProfile.name);
  await fetchStudyGroups(activeProfile.name);
  await fetchStudentInsights(activeProfile.name);
  updateExamBrandCopy(activeProfile);
appendMessage("tutor", "tutor", successMessage || "Your exam list has been updated and your schedule will adapt from the next plan refresh.");
}

async function addExamPlan() {
  if (!activeProfile) {
    return;
  }

  const newExam = normalizeExamEntry({
    name: getExamNameFromInputs(),
    exam_date: examDateInput.value,
    subjects: examSubjectsInput.value,
    portion: examPortionInput.value,
  });
  if (!newExam.name || !newExam.exam_date || !newExam.subjects.length) {
    appendMessage("tutor", "tutor", "Add the exam name, exam date, and at least one subject so I can plan it properly.");
    return;
  }

  const updatedExams = [...(activeProfile.exams || []), newExam];
  if (examCatalogSelect) {
    examCatalogSelect.value = "";
  }
  if (customExamNameInput) {
    customExamNameInput.value = "";
  }
  examDateInput.value = "";
  examSubjectsInput.value = "";
  examPortionInput.value = "";
  examSubjectsInput.readOnly = false;
  updateExamInputMode();
  await saveExamPlans(updatedExams, `${newExam.name} has been added. I will rebalance your upcoming schedules around it.`);
}

async function removeExamPlan(index) {
  if (!activeProfile) {
    return;
  }
  const currentExams = [...(activeProfile.exams || [])];
  const removedExam = currentExams[index];
  const updatedExams = currentExams.filter((_, examIndex) => examIndex !== index);
  await saveExamPlans(
    updatedExams,
    updatedExams.length
      ? `${removedExam.name} has been removed. Your future plans will now focus on the remaining exams.`
      : `${removedExam.name} has been removed. Add a new exam whenever you are ready and I will rebuild your plan.`,
  );
}

async function updateMemory(category, value, action) {
  if (!activeProfile) {
    return;
  }

  const endpoint = action === "remove" ? "/api/memory/remove" : "/api/memory/add";
  const response = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      student_name: activeProfile.name,
      category,
      value,
    }),
  });
  const payload = await response.json();
  if (!response.ok) {
    appendMessage("tutor", "tutor", payload.detail || "I could not update that preference.");
    return;
  }

  renderMemory(payload.personal_memory || {});
  renderMemoryManager(payload.personal_memory || {});
  renderFunFact(payload.fun_fact);
  await fetchStudentInsights(activeProfile.name);
  await fetchStudyGroups(activeProfile.name);
}

async function addInterest() {
  const text = interestManagerInput.value.trim();
  if (!text) {
    return;
  }
  interestManagerInput.value = "";
  await updateMemory("interests", text, "add");
}

async function addPerson() {
  const text = personManagerInput.value.trim();
  if (!text) {
    return;
  }
  personManagerInput.value = "";
  await updateMemory("known_people", text, "add");
}

async function addLifeNote() {
  const text = lifeNoteInput.value.trim();
  if (!text) {
    return;
  }
  lifeNoteInput.value = "";
  await updateMemory("life_notes", text, "add");
}

async function removeMemoryItem(category, value) {
  await updateMemory(category, value, "remove");
}

async function refreshWeeklyPlan() {
  if (!activeProfile) {
    return;
  }
  const response = await fetch(`/api/weekly-plan/${encodeURIComponent(activeProfile.name)}`);
  const payload = await response.json();
  renderWeeklyPlan(payload);
}

async function fetchPhaseStatus(silent = false) {
  if (!activeProfile) {
    return null;
  }
  try {
    const response = await fetch(`/api/phase/status/${encodeURIComponent(activeProfile.name)}`);
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Could not load phase status.");
    }
    latestPhaseStatus = payload;
    return payload;
  } catch (error) {
    if (!silent) {
      setAstraStatus(`Could not load phase status: ${error.message}`, "warning", true);
    }
    return null;
  }
}

async function transitionLearningPhase(silent = true) {
  if (!activeProfile) {
    return null;
  }
  try {
    const response = await fetch(`/api/phase/transition/${encodeURIComponent(activeProfile.name)}`, { method: "POST" });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Could not check phase transition.");
    }
    if (payload.transitioned) {
      await fetchPhaseStatus(true);
      await refreshEngagementAfterLPAward(payload.lp_awards);
      showPhaseTransitionModal(payload);
    }
    return payload;
  } catch (error) {
    if (!silent) {
      setAstraStatus(`Could not check phase transition: ${error.message}`, "warning", true);
    }
    return null;
  }
}

async function refreshTodayPhaseAndBacklog() {
  await fetchPhaseStatus(true);
}

function showPhaseTransitionModal(transition) {
  if (!transition || !transition.transitioned) {
    return;
  }
  const existing = document.querySelector(".phase-transition-modal");
  if (existing) {
    existing.remove();
  }
  const modal = document.createElement("div");
  modal.className = "phase-transition-modal";
  modal.innerHTML = `
    <div class="phase-transition-card" role="dialog" aria-modal="true" aria-label="Phase transition">
      <h3>${transition.new_phase === "phase3_exam_prep" ? "Exam Prep Activated" : "Revision Mode Activated"}</h3>
      <p>${transition.message || "Your study phase has been updated."}</p>
      <button type="button">Continue to Today's Focus</button>
    </div>
  `;
  const close = () => modal.remove();
  modal.querySelector("button").addEventListener("click", close);
  modal.addEventListener("click", (event) => {
    if (event.target === modal) close();
  });
  document.body.appendChild(modal);
}

async function safeStudioStep(stepFn) {
  try {
    await stepFn();
  } catch (error) {
    console.warn("Astra studio step skipped:", error);
  }
}

async function enterLearningStudio(studentName, options = {}) {
  const showIntro = options.showIntro !== false;
  const introMode = options.introMode || "signin";
  profileStatus.textContent = "Loading profile...";
  await fetchAvatarPresets();
  await fetchExamCatalog();
  loadBrowserVoices();

  const response = await fetch(`/api/profile/${encodeURIComponent(studentName)}`);
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || "Could not load profile.");
  }

  activeProfile = payload.profile;
  renderDailyMotivation(activeProfile.name || "");
  applyOnboardingDefaultsToApp(activeProfile);
  if (progressExamInput && (activeProfile.exams || []).length) {
    progressExamInput.value = activeProfile.exams[0].name || "";
  }
  tutorNameInput.value = activeProfile.tutor_name || "Astra";
  applyTutorPersonalityToForm(activeProfile);
  tutorAppearanceInput.value = activeProfile.appearance_description || "";
  updateTutorSummary(activeProfile);
    setTutorMode(activeTutorMode);
    setAvatarStage(payload.active_avatar || avatarPresets[0]);
    void initAvatar();
    renderTutorBrain(payload.tutor_brain || buildLocalTutorBrain(activeProfile, payload.active_avatar || avatarPresets[0], "tutor"));
  renderMemory(payload.personal_memory || {});
  renderMemoryManager(payload.personal_memory || {});
  renderExamManager(activeProfile.exams || []);
  renderFunFact(payload.fun_fact);
  const studioSteps = [
    () => fetchMotivationSection(),
    () => fetchLearningSources(activeProfile.name),
    () => fetchVideoLibrary(activeProfile.name),
    () => fetchStudyGroups(activeProfile.name),
    () => fetchProgress(activeProfile.name),
    () => fetchPracticeAnalytics(activeProfile.name),
    () => fetchEngagement(activeProfile.name),
    () => fetchStudentInsights(activeProfile.name),
    () => fetchStorageStatus(activeProfile.name),
    () => fetchSyllabusDocuments(activeProfile.name),
    () => fetchTutorConversations(),
    () => fetchLoungeConversations(),
    () => fetchChatHistory("practice"),
    () => refreshActiveChapterSession(),
    () => loadChapterResumeState(true),
  ];
  await Promise.allSettled(studioSteps.map((step) => safeStudioStep(step)));
  renderJourneySetup(journeyPlanSnapshot);
  renderLiveSources([]);
  renderVisualLearning(null);
  renderVideoExplanation(null);
  renderReasoningPanel(null);
  renderSummaryPanel("");
  preferTutorVideosForAvatar(payload.active_avatar || avatarPresets[0]);
  renderAdaptiveProfile((payload.weekly_plan && payload.weekly_plan.adaptive_profile) || null);
  renderAvatars(activeProfile.selected_avatar);
  renderHomeTutorPersonalityGrid();
  await refreshWeeklyPlan();
  await safeStudioStep(() => fetchPhaseStatus(true));
  const phaseTransition = await transitionLearningPhase(true);
  await safeStudioStep(() => refreshTodayPhaseAndBacklog());
  applyTabOrder();
  setHomeSubtab("overview");
  setCaption("No speech playing right now.");
  applyExplanationPreferences();
  applyLeagueVisibility();
  updateExamBrandCopy(activeProfile);
  if (journeyHoursInput && activeProfile.max_study_hours_per_day) {
    journeyHoursInput.value = String(activeProfile.max_study_hours_per_day);
  }
  renderJourneySetup(journeyPlanSnapshot);

  if (studentWelcome) {
    studentWelcome.textContent = `Welcome, ${activeProfile.name}`;
  }
  const exams = getActiveExamListLabel(activeProfile);
  if (studentSubcopy) {
    studentSubcopy.textContent = exams
      ? `Start with your tutor first, then move into ${exams} at your own pace.`
      : `Start with your tutor first, then add ${getActiveExamLabel(activeProfile)} in Personalize whenever you are ready.`;
  }
  if (showIntro) {
    openIntroScreen(activeProfile, introMode);
  } else {
    if (introScreen) {
      introScreen.classList.add("hidden");
    }
    loginScreen.classList.add("hidden");
    appShell.classList.remove("hidden");
    pendingPlanSubtab = "today";
    setActiveTab("weeklyTab");
    setPlanSubtab("today");
    if (phaseTransition && phaseTransition.transitioned) {
      showPhaseTransitionModal(phaseTransition);
    }
  }
  if (activeProfile.jee_mvp_initialized && activeProfile.legacy_exam_scope && activeProfile.legacy_exam_scope.length) {
    appendMessage(
      "tutor",
      "tutor",
      `This MVP is currently running in ${getActiveExamLabel(activeProfile)}-first mode, so I have switched your active study scope to the active exam flow for the demo. Your older exam setup is preserved in the background and can be restored later.`
    );
  }
  if (!(activeProfile.exams || []).length) {
    appendMessage("tutor", "tutor", `Welcome in. Whenever you are ready, open Personalize and add ${getActiveExamLabel(activeProfile)} so I can build your prep plan properly.`);
  }
}

async function loadProfile() {
  const email = signinEmailInput.value.trim();
  const password = signinPasswordInput.value;
  if (!email || !password) {
    profileStatus.textContent = "Enter your email and password first.";
    return;
  }

  profileStatus.textContent = "Signing you in...";
  loadProfileBtn.disabled = true;
  try {
    const response = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email,
        password,
      }),
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Could not sign in.");
    }

    persistAuthSession(payload.session || null, payload.user || null);
    await enterLearningStudio((payload.profile && payload.profile.name) || (payload.user && payload.user.student_name) || "", { showIntro: false });
  } catch (error) {
    profileStatus.textContent = error.message;
  } finally {
    loadProfileBtn.disabled = false;
  }
}

async function createWebProfile() {
  const displayName = signupName.value.trim();
  const email = signupEmail.value.trim();
  const password = signupPassword.value;
  const studentName = signupStudentName.value.trim();
  const maxStudyHours = Number(signupHours.value || "4");

  if (!displayName || !email || !password) {
    profileStatus.textContent = "Enter your name, email, and password first.";
    return;
  }

  profileStatus.textContent = "Creating your account...";
  createProfileBtn.disabled = true;
  try {
    const response = await fetch("/api/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        display_name: displayName,
        email,
        password,
        student_name: studentName,
        max_study_hours_per_day: maxStudyHours,
        onboarding_why_astra: signupWhyAstra ? signupWhyAstra.value.trim() : "",
        onboarding_interests: signupInterests ? signupInterests.value.trim() : "",
        onboarding_dislikes: signupDislikes ? signupDislikes.value.trim() : "",
        onboarding_conversation_style: signupConversationStyle ? signupConversationStyle.value.trim() : "",
        onboarding_preferred_language: languageSelect ? languageSelect.value.trim() : currentLanguage,
        onboarding_explanation_depth: tutorLevelSelect ? String(tutorLevelSelect.value || "3") : "3",
        onboarding_stress_support: signupStressSupport ? signupStressSupport.value.trim() : "",
        onboarding_goals_summary: signupGoalsSummary ? signupGoalsSummary.value.trim() : "",
        onboarding_astra_question: walkthroughAnswers.astra_question || "",
        onboarding_astra_question_answer: walkthroughAnswers.astra_question_answer || "",
      }),
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Could not create account.");
    }

    persistAuthSession(payload.session || null, payload.user || null);
    signinEmailInput.value = email;
    signinPasswordInput.value = "";
    await enterLearningStudio((payload.profile && payload.profile.name) || (payload.user && payload.user.student_name) || displayName, { introMode: "signup" });
  } catch (error) {
    profileStatus.textContent = error.message;
  } finally {
    createProfileBtn.disabled = false;
  }
}

function readFileAsBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const result = String(reader.result || "");
      const base64 = result.includes(",") ? result.split(",")[1] : result;
      resolve(base64);
    };
    reader.onerror = () => reject(new Error("Could not read that image file."));
    reader.readAsDataURL(file);
  });
}

async function handleDoubtImageSelection() {
  const file = doubtImageInput && doubtImageInput.files && doubtImageInput.files[0];
  if (!file) {
    pendingDoubtImage = null;
    imageUploadStatus.textContent = "Upload a picture of your doubt, worksheet, or handwritten solution.";
    return;
  }

  imageUploadStatus.textContent = `Preparing ${file.name}...`;
  const base64 = await readFileAsBase64(file);
  pendingDoubtImage = {
    base64,
    mimeType: file.type || "image/png",
    fileName: file.name,
  };
  imageUploadStatus.textContent = `${file.name} is ready. Click "Scan doubt image" to send it to the tutor.`;
}

async function analyzeDoubtImage() {
  if (!activeProfile) {
    return;
  }
  if (!pendingDoubtImage) {
    imageUploadStatus.textContent = "Choose an image first.";
    return;
  }

  const prompt = messageInput.value.trim();
  interruptTutorOutput("tutor");
  appendMessage("tutor", "student", prompt || `Uploaded image: ${pendingDoubtImage.fileName}`);
  analyzeImageBtn.disabled = true;
  imageUploadStatus.textContent = "Analyzing your doubt image...";
  try {
    const response = await fetch("/api/chat/image", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        student_name: activeProfile.name,
        message: prompt,
        image_base64: pendingDoubtImage.base64,
        mime_type: pendingDoubtImage.mimeType,
        response_language: currentLanguage,
        conversation_id: activeTutorConversationId,
      }),
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Could not analyze that image.");
    }

      lastTutorReply = payload.reply;
      onTutorReplyReceived(payload.reply);
      lastRepliesByMode.tutor = payload.reply;
    if (payload.conversation_id) {
      activeTutorConversationId = payload.conversation_id;
      renderTutorConversations(payload.conversations || []);
    }
    streamTutorReply("tutor", payload.reply);
    renderTutorBrain(payload.tutor_brain || buildLocalTutorBrain(activeProfile, payload.active_avatar || activeAvatar, "tutor"));
    renderVisualLearning(payload.visual_learning || null);
    renderVideoExplanation(payload.video_explanation || null);
    renderReasoningPanel(payload.video_explanation || null);
    renderAdaptiveProfile(payload.adaptive_profile || null);
    renderFunFact(payload.fun_fact);
    renderMemory(payload.personal_memory || {});
    renderMemoryManager(payload.personal_memory || {});
    if (autoSpeakReplies.checked && !payload.video_explanation) {
      speakText(payload.reply);
    }
    await fetchStorageStatus(activeProfile.name);
    messageInput.value = "";
    doubtImageInput.value = "";
    pendingDoubtImage = null;
    imageUploadStatus.textContent = "Image analyzed. You can upload another doubt whenever you want.";
  } catch (error) {
    appendMessage("tutor", "tutor", `Something went wrong: ${error.message}`);
    imageUploadStatus.textContent = error.message;
  } finally {
    analyzeImageBtn.disabled = false;
  }
}

async function sendMessage(message) {
  if (!activeProfile || isSending) {
    return;
  }

  isSending = true;
  lastTutorQuestion = message;
  const activeTabElement = document.querySelector(".tab-panel.active");
  const activeTab = activeTabElement ? activeTabElement.id : "tutorTab";
  const mode = activeTab === "guideTab"
    ? "guide"
    : activeTab === "loungeTab"
    ? "lounge"
    : activeTab === "practiceTab"
    ? "practice"
    : activeTab === "lastMinuteTab"
    ? "last_minute"
    : activeTab === "tipsTab"
    ? "tips"
    : "tutor";
  interruptTutorOutput(mode);
  appendMessage(mode, "student", message);
  if (mode === "tutor") {
    renderVideoAnswerBrief(null);
  }
  const activeFocus = getActiveTutorFocus();
  if (mode === "tutor") {
    setAstraStatus(`Astra is explaining ${activeFocus.topic}...`, "working");
    showKnowledgeBaseTag(`Searching NCERT ${activeFocus.subject}...`, true);
    logSessionActivity(`Asked about ${activeFocus.topic}`);
  } else {
    setAstraStatus("Astra is working...", "working");
  }
  if (messageInput) {
    messageInput.disabled = true;
  }
  if (guideMessageInput) {
    guideMessageInput.disabled = true;
  }
  if (loungeMessageInput) {
    loungeMessageInput.disabled = true;
  }
  if (lastMinuteMessageInput) {
    lastMinuteMessageInput.disabled = true;
  }
  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        student_name: activeProfile.name,
        message,
        voice_chat_mode: voiceChatMode.checked,
        response_language: currentLanguage,
        conversation_mode: mode,
        tutor_mode: activeTutorMode,
        tutor_level: Number((tutorLevelSelect && tutorLevelSelect.value) || "3"),
        reading_comfort_mode: !!(readingComfortMode && readingComfortMode.checked),
        chunked_reply_mode: !!(chunkedReplyMode && chunkedReplyMode.checked),
        response_pacing: (responsePacingSelect && responsePacingSelect.value) || "gentle",
        conversation_id: mode === "tutor" ? activeTutorConversationId : mode === "lounge" ? activeLoungeConversationId : null,
      }),
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Could not get tutor response.");
    }

      lastTutorReply = payload.reply;
      onTutorReplyReceived(payload.reply);
      lastRepliesByMode[mode] = payload.reply;
    if (mode === "tutor" && payload.conversation_id) {
      activeTutorConversationId = payload.conversation_id;
      renderTutorConversations(payload.conversations || []);
    } else if (mode === "lounge" && payload.conversation_id) {
      activeLoungeConversationId = payload.conversation_id;
      renderLoungeConversations(payload.conversations || []);
    }
    const replyStream = streamTutorReply(mode, payload.reply);

    if (payload.active_avatar) {
      setAvatarStage(payload.active_avatar);
      renderAvatars(activeProfile.selected_avatar);
      renderHomeTutorPersonalityGrid();
    }
    renderTutorBrain(payload.tutor_brain || buildLocalTutorBrain(activeProfile, payload.active_avatar || activeAvatar, mode));
    renderMemory(payload.personal_memory || {});
    renderMemoryManager(payload.personal_memory || {});
    renderFunFact(payload.fun_fact);
    renderLiveSources(payload.live_sources || []);
    if (mode === "tutor") {
      const suggestedTopic = _inferVideoTopicFromText(
        (payload.visual_learning && payload.visual_learning.title)
        || (payload.video_explanation && payload.video_explanation.title)
        || payload.reply
        || message
      );
      const suggestedSubject = _inferVideoSubjectFromText(
        (payload.visual_learning && payload.visual_learning.title)
        || (payload.video_explanation && payload.video_explanation.title)
        || message
      );
      if (suggestedTopic && suggestedTopic !== "the topic" && suggestedTopic !== "this topic") {
        updateAstraCurrentTopic(suggestedTopic, suggestedSubject, "tutor");
      }
      renderVisualLearning(payload.visual_learning || null);
      renderVideoExplanation(payload.video_explanation || null);
      renderReasoningPanel(payload.video_explanation || null);
    } else if (mode === "practice" || mode === "tips" || mode === "guide" || mode === "last_minute") {
      renderVisualLearning(null);
      renderVideoExplanation(null);
      renderReasoningPanel(null);
    }
    if (payload.reply_type === "weekly_plan" && payload.weekly_plan) {
      renderWeeklyPlan(payload.weekly_plan);
    }
    if (mode === "tutor") {
      renderAdaptiveProfile(payload.adaptive_profile || ((payload.weekly_plan && payload.weekly_plan.adaptive_profile) || null));
    }
    await fetchStudentInsights(activeProfile.name);
    if (mode === "tutor") {
      logSessionActivity(`Astra answered ${activeFocus.topic}`);
    }
    const shouldSpeakReply = autoSpeakReplies.checked;
    if (shouldSpeakReply) {
      speakText(payload.reply);
    } else if (autoCaptionMode.checked && mode === "tutor") {
      setCaption(payload.reply);
    }
    await replyStream;
    showKnowledgeBaseTag("", false);
    if (mode === "tutor") {
      const suggestedTopic = _inferVideoTopicFromText(
        (payload.visual_learning && payload.visual_learning.title)
        || (payload.video_explanation && payload.video_explanation.title)
        || payload.reply
        || message
      );
      const suggestedSubject = _inferVideoSubjectFromText(
        (payload.visual_learning && payload.visual_learning.title)
        || (payload.video_explanation && payload.video_explanation.title)
        || message
      );
      if (suggestedTopic && suggestedTopic !== "the topic" && suggestedTopic !== "this topic") {
        renderVideoSuggestionCard(suggestedTopic, suggestedSubject);
      }
      await refreshActiveChapterSession();
      const explanationLevel = Number((tutorLevelSelect && tutorLevelSelect.value) || activeProfile.default_tutor_level || "3");
      const chapterActive = isChapterCheckpointActive();
      const checkpointTopic = chapterActive
        ? (activeChapterSubtopic.subtopic_name || activeChapterSubtopic.chapter_name || message)
        : ((payload.visual_learning && payload.visual_learning.title)
          || (payload.video_explanation && payload.video_explanation.topic)
          || message);
      const checkpointSubject = chapterActive
        ? (activeChapterSubtopic.subject || ((activeProfile.exams && activeProfile.exams[0] && activeProfile.exams[0].subjects && activeProfile.exams[0].subjects[0]) || ""))
        : ((payload.visual_learning && payload.visual_learning.subject)
          || (payload.video_explanation && payload.video_explanation.subject)
          || ((activeProfile.exams && activeProfile.exams[0] && activeProfile.exams[0].subjects && activeProfile.exams[0].subjects[0]) || ""));
      await new Promise((resolve) => window.setTimeout(resolve, 1000));
      await loadTutorCheckpoint(
        checkpointTopic,
        checkpointSubject,
        explanationLevel,
        payload.reply,
        chapterActive ? { chapterMode: true } : {},
      );
    }
    await fetchStorageStatus(activeProfile.name);
    setAstraStatus(
      mode === "tutor"
        ? `Astra is ready. Today's focus: ${activeFocus.topic} - ${activeFocus.subject}`
        : "Astra is ready.",
      "success",
      true
    );
  } catch (error) {
    appendMessage(mode, "tutor", `Something went wrong: ${error.message}`);
    setAstraStatus(`Could not respond: ${error.message}`, "warning", true);
    showKnowledgeBaseTag("", false);
  } finally {
    isSending = false;
    if (messageInput) {
      messageInput.disabled = false;
    }
    if (loungeMessageInput) {
      loungeMessageInput.disabled = false;
    }
    if (guideMessageInput) {
      guideMessageInput.disabled = false;
    }
    if (lastMinuteMessageInput) {
      lastMinuteMessageInput.disabled = false;
    }
  }
}

document.body.addEventListener("click", (event) => {
  const studioPaneButton = event.target.closest(".studio-pane-button");
  if (studioPaneButton) {
    setActiveStudioPane(studioPaneButton.dataset.studioPane);
  }

  const languageCardButton = event.target.closest(".language-card");
  if (languageCardButton) {
    setLanguagePreference(languageCardButton.dataset.language || "english", {
      persist: true,
      updateProfile: true,
      showConfirmation: true,
    });
  }

  const languageChipButton = event.target.closest("#tutorLanguageChip");
  if (languageChipButton && tutorLanguageDropdown) {
    tutorLanguageDropdown.classList.toggle("hidden");
  }

  const languageOptionButton = event.target.closest("[data-language-option]");
  if (languageOptionButton) {
    if (tutorLanguageDropdown) {
      tutorLanguageDropdown.classList.add("hidden");
    }
    setLanguagePreference(languageOptionButton.dataset.languageOption || "english", {
      persist: true,
      updateProfile: true,
      showConfirmation: true,
    });
  }

  if (tutorLanguageDropdown && !event.target.closest(".tutor-language-picker")) {
    tutorLanguageDropdown.classList.add("hidden");
  }

  const homeSubtabButton = event.target.closest("[data-home-subtab]");
  if (homeSubtabButton) {
    if (document.querySelector("#overviewTab") && !document.querySelector("#overviewTab").classList.contains("active")) {
      setActiveTab("overviewTab");
    }
    setHomeSubtab(homeSubtabButton.dataset.homeSubtab);
  }

  const tabButton = event.target.closest(".tab-button");
  if (tabButton) {
    setActiveTab(tabButton.dataset.tab);
  }

  if (event.target.closest("#motivationQuickAccessBtn") && motivationSection) {
    setActiveTab("overviewTab");
    setHomeSubtab("motivation");
    if (motivationSection) {
      motivationSection.open = true;
      motivationSection.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }

  if (event.target.closest("#talkToAstraInLoungeBtn")) {
    setActiveTab("loungeTab");
    if (loungeMessageInput) {
      loungeMessageInput.value = "I am feeling overwhelmed and need some support";
      window.setTimeout(() => loungeMessageInput.focus(), 0);
    }
  }

  if (event.target.closest("#dismissDailyBriefingBtn")) {
    dailyBriefingDismissedDate = new Date().toISOString().slice(0, 10);
    if (dailyBriefingCard) {
      dailyBriefingCard.classList.add("hidden");
    }
  }

  if (event.target.closest("#overviewStartLearningBtn")) {
    startTodaySessionFromHome();
  }

  if (event.target.closest("#continueJourneyBtn")) {
    startTodaySessionFromHome();
  }

  if (event.target.closest("#openPracticeFromHomeBtn")) {
    setActiveTab("practiceTab");
  }

  if (event.target.closest("#needHelpConceptBtn")) {
    focusTutorComposerWithPrompt(`Explain ${getActiveTutorFocus().topic} from the beginning`);
  }

  if (event.target.closest("#openProgressFromHomeBtn")) {
    openPlanSubtab("progress");
  }

  const tutorIntentChip = event.target.closest(".tutor-intent-chip");
  if (tutorIntentChip) {
    const intent = tutorIntentChip.dataset.tutorIntent || "doubt";
    const focus = getActiveTutorFocus();
    if (intent === "journey") {
      startTodaySessionFromHome();
    } else if (intent === "practice") {
      setActiveTab("practiceTab");
    } else {
      focusTutorComposerWithPrompt(
        focus.topic ? `I want help with ${focus.topic}` : "I want help with a concept"
      );
    }
  }

  if (event.target.closest("#sessionActivityToggleBtn") && sessionActivityPanel) {
    const shouldHide = !sessionActivityPanel.classList.contains("hidden");
    sessionActivityPanel.classList.toggle("hidden", shouldHide);
    if (sessionActivityToggleBtn) {
      sessionActivityToggleBtn.textContent = shouldHide ? "Session log >" : "Session log v";
    }
  }

  if (event.target.closest("#motivationReadStoryBtn")) {
    motivationStoryOpen = !motivationStoryOpen;
    renderMotivationStory(activeMotivationStoryIndex);
  }

  if (event.target.closest("#motivationPrevStoryBtn")) {
    motivationStoryOpen = true;
    renderMotivationStory(activeMotivationStoryIndex - 1);
  }

  if (event.target.closest("#motivationNextStoryBtn")) {
    motivationStoryOpen = true;
    renderMotivationStory(activeMotivationStoryIndex + 1);
  }


  const commandButton = event.target.closest("[data-command]");
  if (commandButton) {
    if (commandButton.dataset.command === "Show weekly plan") {
      openPlanSubtab("thisweek");
    }
    sendMessage(commandButton.dataset.command);
  }

  const checkinButton = event.target.closest("[data-checkin]");
  if (checkinButton) {
    setActiveTab("tutorTab");
    sendMessage(checkinButton.dataset.checkin);
  }

  const starterButton = event.target.closest("[data-starter]");
  if (starterButton) {
    setActiveTab("loungeTab");
    sendMessage(starterButton.dataset.starter);
  }

  const practicePromptButton = event.target.closest("[data-practice-prompt]");
  if (practicePromptButton) {
    lastPracticeMode = (practicePromptButton.dataset.practiceMode || practicePromptButton.textContent.trim().toLowerCase()).trim();
    if (practicePromptButton.dataset.practiceMode === "diagnostic mock") {
      if (mockTestExamInput && activeProfile && activeProfile.exams && activeProfile.exams.length) {
        mockTestExamInput.value = activeProfile.exams[0].name || mockTestExamInput.value || APP_CONFIG.default_exam || "JEE Main";
      }
      setActiveTab("mockTestTab");
      if (mockTestStatus) {
        mockTestStatus.textContent = "Astra has opened the mock test room. Start the baseline when you are ready.";
      }
      return;
    }
    setActiveTab("practiceTab");
    sendMessage(practicePromptButton.dataset.practicePrompt);
  }

  const lastMinutePromptButton = event.target.closest("[data-last-minute-prompt]");
  if (lastMinutePromptButton) {
    setActiveTab("lastMinuteTab");
    sendMessage(lastMinutePromptButton.dataset.lastMinutePrompt);
  }

  const guidePromptButton = event.target.closest("[data-guide-prompt]");
  if (guidePromptButton) {
    setActiveTab("guideTab");
    sendMessage(guidePromptButton.dataset.guidePrompt);
  }

  const tipsPromptButton = event.target.closest("[data-tips-prompt]");
  if (tipsPromptButton) {
    setActiveTab("tipsTab");
    sendMessage(tipsPromptButton.dataset.tipsPrompt);
  }

  const tutorPromptButton = event.target.closest("[data-tutor-prompt]");
  if (tutorPromptButton) {
    setActiveTab("tutorTab");
    sendMessage(tutorPromptButton.dataset.tutorPrompt);
  }

  const hobbyButton = event.target.closest("[data-hobby]");
  if (hobbyButton) {
    setActiveTab("loungeTab");
    sendMessage(hobbyButton.dataset.hobby);
  }

  const themeButton = event.target.closest("[data-theme]");
  if (themeButton) {
    currentTheme = themeButton.dataset.theme;
    applyThemePreferences();
  }

  const backgroundButton = event.target.closest("[data-background]");
  if (backgroundButton) {
    currentBackground = backgroundButton.dataset.background;
    applyThemePreferences();
  }

  const timerButton = event.target.closest("[data-timer-minutes]");
  if (timerButton) {
    const minutes = Number(timerButton.dataset.timerMinutes || "0");
    if (minutes > 0) {
      startLoungeTimer(minutes);
    }
  }

  const progressButton = event.target.closest("[data-progress-id][data-progress-status]");
  if (progressButton) {
    updateProgressItemStatus(progressButton.dataset.progressId, progressButton.dataset.progressStatus);
  }
});

loadProfileBtn.addEventListener("click", loadProfile);
showSigninBtn.addEventListener("click", () => setAuthMode("signin"));
showSignupBtn.addEventListener("click", () => {
  setAuthMode("signup");
  openWalkthrough("signup");
});
if (openSignupWalkthroughBtn) {
  openSignupWalkthroughBtn.addEventListener("click", () => openWalkthrough("signup"));
}
if (skipSignupWalkthroughBtn) {
  skipSignupWalkthroughBtn.addEventListener("click", closeWalkthrough);
}
createProfileBtn.addEventListener("click", createWebProfile);
if (jumpToTutorBtn) {
  jumpToTutorBtn.addEventListener("click", () => setActiveTab("tutorTab"));
}
if (startWalkWithAstraBtn) {
  startWalkWithAstraBtn.addEventListener("click", () => openWalkthrough("existing", activeProfile));
}
if (editWalkWithAstraBtn) {
  editWalkWithAstraBtn.addEventListener("click", () => openWalkthrough("existing", activeProfile));
}
if (walkthroughBackBtn) {
  walkthroughBackBtn.addEventListener("click", () => advanceWalkthrough(-1));
}
if (walkthroughNextBtn) {
  walkthroughNextBtn.addEventListener("click", async () => {
    if (walkthroughStepIndex >= WALKTHROUGH_STEPS.length - 1) {
      try {
        await saveWalkthrough();
        if (walkthroughContext === "signup") {
          profileStatus.textContent = "Walkthrough saved. You can now create your account or continue editing.";
        } else if (activeProfile) {
          await fetchStudyGroups(activeProfile.name);
          await fetchStudentInsights(activeProfile.name);
          profileStatus.textContent = "Walkthrough saved to your profile.";
        }
      } catch (error) {
        if (profileStatus) {
          profileStatus.textContent = error.message;
        }
      }
      return;
    }
    advanceWalkthrough(1);
  });
}
if (walkthroughSaveBtn) {
  walkthroughSaveBtn.addEventListener("click", async () => {
    try {
      await saveWalkthrough();
      if (walkthroughContext === "signup") {
        applyWalkthroughAnswersToSignupFields();
        profileStatus.textContent = "Walkthrough saved. You can now create your account or continue editing.";
      } else if (activeProfile) {
        await fetchStudyGroups(activeProfile.name);
        await fetchStudentInsights(activeProfile.name);
        profileStatus.textContent = "Walkthrough saved to your profile.";
      }
    } catch (error) {
      if (profileStatus) {
        profileStatus.textContent = error.message;
      }
    }
  });
}
if (walkthroughSkipBtn) {
  walkthroughSkipBtn.addEventListener("click", closeWalkthrough);
}
if (walkthroughCloseBtn) {
  walkthroughCloseBtn.addEventListener("click", closeWalkthrough);
}
if (walkthroughBackdrop) {
  walkthroughBackdrop.addEventListener("click", closeWalkthrough);
}
if (walkthroughInput) {
  walkthroughInput.addEventListener("input", () => {
    const currentStep = WALKTHROUGH_STEPS[walkthroughStepIndex] || WALKTHROUGH_STEPS[0];
    walkthroughAnswers[currentStep.key] = walkthroughInput.value;
    if (currentStep.key === "astra_question") {
      walkthroughAnswers.astra_question_answer = buildWalkthroughAstraAnswer(walkthroughInput.value);
      setWalkthroughAnswerText(walkthroughAnswers.astra_question_answer);
    }
  });
}
if (askAstraBtn) {
  askAstraBtn.addEventListener("click", askAstraAboutItself);
}
if (logoutBtn) {
  logoutBtn.addEventListener("click", logoutAndShowAuth);
}

if (studioMenuToggleBtn) {
  studioMenuToggleBtn.addEventListener("click", () => {
    isSidebarCollapsed = !isSidebarCollapsed;
    applySidebarState();
  });
}
if (openVideoBridgeBtn) {
  openVideoBridgeBtn.addEventListener("click", () => {
    openActiveTutorVideoBridge();
  });
}
if (useVideoInTutorBtn) {
  useVideoInTutorBtn.addEventListener("click", () => {
    useActiveTutorVideoInTutor();
  });
}
if (authHeroVideoToggle) {
  authHeroVideoToggle.addEventListener("click", toggleAuthHeroVideoPlayback);
}
if (introContinueBtn) {
  introContinueBtn.addEventListener("click", enterStudioFromIntro);
}
if (introSoundBtn) {
  introSoundBtn.addEventListener("click", toggleIntroVideoSound);
}
if (introVideoToggle) {
  introVideoToggle.addEventListener("click", toggleIntroVideoPlayback);
}
if (fullscreenStudioBtn) {
  fullscreenStudioBtn.addEventListener("click", toggleStudioFullscreen);
}
if (tutorFullscreenBtn) {
  tutorFullscreenBtn.addEventListener("click", toggleTutorFullscreen);
  _setTutorFullscreenButtonState(false);
}
if (loungeFullscreenBtn) {
  loungeFullscreenBtn.addEventListener("click", toggleLoungeFullscreen);
  _setLoungeFullscreenButtonState(false);
}
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    closeTutorFullscreen();
    closeLoungeFullscreen();
    if (chapterDetailCard && !chapterDetailCard.classList.contains("hidden")) {
      closeChapterDetailPanel();
    }
  }
});
if (chapterDetailCloseBtn) {
  chapterDetailCloseBtn.addEventListener("click", closeChapterDetailPanel);
}
if (journeyHoursInput && journeyHoursLabel) {
  journeyHoursInput.addEventListener("input", () => {
    journeyHoursLabel.textContent = _formatJourneyHours(journeyHoursInput.value);
  });
}
if (setupJourneyBtn) {
  setupJourneyBtn.addEventListener("click", async () => {
    await setupJourneyFromUI();
  });
}
if (journeyExamDateSaveBtn) {
  journeyExamDateSaveBtn.addEventListener("click", () => {
    if (!journeyExamDateInput || !journeyExamDateInput.value) {
      alert("Please select your exam date before continuing");
      return;
    }
    if (journeySetupStatus) {
      journeySetupStatus.textContent = "Exam date saved. Click Begin My Journey when you are ready.";
    }
  });
}
if (beginJourneyBtn) {
  beginJourneyBtn.addEventListener("click", async () => {
    if (journeyPlanSnapshot) {
      await startJourneySession();
    } else {
      await setupJourneyFromUI();
      if (journeyPlanSnapshot) {
        await startJourneySession();
      }
    }
  });
}
if (startSessionBtn) {
  startSessionBtn.addEventListener("click", async () => {
    await startJourneySession();
  });
}
if (openJourneySummaryBtn) {
  openJourneySummaryBtn.addEventListener("click", () => {
    openPlanSubtab("journey");
    window.setTimeout(() => {
      if (journeyProgressSidebar && typeof journeyProgressSidebar.scrollIntoView === "function") {
        journeyProgressSidebar.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    }, 0);
  });
}
if (startChapterSessionBtn) {
  startChapterSessionBtn.addEventListener("click", async () => {
    await startSelectedChapterSession();
  });
}
if (clearTutorChatBtn) {
  clearTutorChatBtn.addEventListener("click", async () => {
    try {
      await deleteChatHistory("tutor");
    } catch (error) {
      appendMessage("tutor", "tutor", error.message);
    }
  });
}
if (newTutorChatBtn) {
  newTutorChatBtn.addEventListener("click", async () => {
    try {
      await createTutorConversation();
    } catch (error) {
      appendMessage("tutor", "tutor", error.message);
    }
  });
}
if (viewAllTutorChatsBtn) {
  viewAllTutorChatsBtn.addEventListener("click", async () => {
    try {
      await fetchTutorConversations();
      openTutorConversationDrawer();
    } catch (error) {
      appendMessage("tutor", "tutor", error.message);
    }
  });
}
if (closeTutorConversationDrawerBtn) {
  closeTutorConversationDrawerBtn.addEventListener("click", closeTutorConversationDrawer);
}
if (tutorConversationDrawerBackdrop) {
  tutorConversationDrawerBackdrop.addEventListener("click", closeTutorConversationDrawer);
}
document.addEventListener("click", (event) => {
  const dropdown = document.getElementById("recent-chats-dropdown");
  if (!dropdown) {
    return;
  }
  if (!event.target.closest(".recent-chats-compact")) {
    dropdown.classList.add("hidden");
  }
});
if (loungeTimerToggleBtn && loungeTimerPanel) {
  loungeTimerToggleBtn.addEventListener("click", () => {
    const willOpen = loungeTimerPanel.classList.contains("hidden");
    setLoungePopover(loungeHistoryPanel, loungeHistoryToggleBtn, false);
    setLoungePopover(loungeTimerPanel, loungeTimerToggleBtn, willOpen);
  });
}
if (loungeHistoryToggleBtn && loungeHistoryPanel) {
  loungeHistoryToggleBtn.addEventListener("click", () => {
    const willOpen = loungeHistoryPanel.classList.contains("hidden");
    setLoungePopover(loungeTimerPanel, loungeTimerToggleBtn, false);
    setLoungePopover(loungeHistoryPanel, loungeHistoryToggleBtn, willOpen);
  });
}
if (closeLoungeHistoryBtn) {
  closeLoungeHistoryBtn.addEventListener("click", () => {
    setLoungePopover(loungeHistoryPanel, loungeHistoryToggleBtn, false);
  });
}
if (loungeDeletedToggleBtn && loungeDeletedPanel) {
  loungeDeletedToggleBtn.addEventListener("click", () => {
    const willOpen = loungeDeletedPanel.classList.contains("hidden");
    loungeDeletedPanel.classList.toggle("hidden", !willOpen);
    loungeDeletedToggleBtn.setAttribute("aria-expanded", willOpen ? "true" : "false");
  });
}

if (newLoungeChatBtn) {
  newLoungeChatBtn.addEventListener("click", async () => {
    try {
      await createLoungeConversation();
      closeLoungePanels();
    } catch (error) {
      appendMessage("lounge", "tutor", error.message);
    }
  });
}
if (tutorChatSearchInput) {
  tutorChatSearchInput.addEventListener("input", async () => {
    tutorConversationSearch = tutorChatSearchInput.value.trim();
    try {
      await fetchTutorConversations();
    } catch (error) {
      appendMessage("tutor", "tutor", error.message);
    }
  });
}
if (loungeChatSearchInput) {
  loungeChatSearchInput.addEventListener("input", async () => {
    loungeConversationSearch = loungeChatSearchInput.value.trim();
    try {
      await fetchLoungeConversations();
    } catch (error) {
      appendMessage("lounge", "tutor", error.message);
    }
  });
}
if (loungeConversationSelect) {
  loungeConversationSelect.addEventListener("change", async () => {
    const nextId = Number(loungeConversationSelect.value);
    if (!Number.isFinite(nextId) || !nextId) {
      return;
    }
    activeLoungeConversationId = nextId;
    setLoungeActionState(getSelectedLoungeConversation());
    try {
      await fetchChatHistory("lounge", activeLoungeConversationId);
    } catch (error) {
      appendMessage("lounge", "tutor", error.message);
    }
  });
}
if (loungeRenameChatBtn) {
  loungeRenameChatBtn.addEventListener("click", async () => {
    const conversation = getSelectedLoungeConversation();
    if (!conversation) {
      return;
    }
    const nextTitle = window.prompt("Rename this lounge chat", conversation.title || "New chat");
    if (nextTitle === null) {
      return;
    }
    try {
      await updateConversationByMode("lounge", conversation.id, { title: nextTitle });
    } catch (error) {
      appendMessage("lounge", "tutor", error.message);
    }
  });
}
if (loungePinChatBtn) {
  loungePinChatBtn.addEventListener("click", async () => {
    const conversation = getSelectedLoungeConversation();
    if (!conversation) {
      return;
    }
    try {
      await updateConversationByMode("lounge", conversation.id, { pinned: !conversation.pinned_at });
    } catch (error) {
      appendMessage("lounge", "tutor", error.message);
    }
  });
}
if (loungeDeleteChatBtn) {
  loungeDeleteChatBtn.addEventListener("click", async () => {
    const conversation = getSelectedLoungeConversation();
    if (!conversation) {
      return;
    }
    const ok = window.confirm(`Delete "${conversation.title || "New chat"}"? You can recover it from Recently Deleted.`);
    if (!ok) {
      return;
    }
    activeLoungeConversationId = conversation.id;
    try {
      await deleteChatHistory("lounge");
    } catch (error) {
      appendMessage("lounge", "tutor", error.message);
    }
  });
}
if (deletedLoungeConversationSelect) {
  deletedLoungeConversationSelect.addEventListener("change", () => {
    const selected = getSelectedDeletedLoungeConversation();
    if (restoreLoungeChatBtn) {
      restoreLoungeChatBtn.disabled = !selected;
    }
  });
}
if (restoreLoungeChatBtn) {
  restoreLoungeChatBtn.addEventListener("click", async () => {
    const conversation = getSelectedDeletedLoungeConversation();
    if (!conversation) {
      return;
    }
    try {
      await restoreConversationByMode("lounge", conversation.id);
    } catch (error) {
      appendMessage("lounge", "tutor", error.message);
    }
  });
}
if (clearPracticeChatBtn) {
  clearPracticeChatBtn.addEventListener("click", async () => {
    try {
      await deleteChatHistory("practice");
    } catch (error) {
      appendMessage("practice", "tutor", error.message);
    }
  });
}
if (clearLoungeChatBtn) {
  clearLoungeChatBtn.addEventListener("click", async () => {
    try {
      await deleteChatHistory("lounge");
    } catch (error) {
      appendMessage("lounge", "tutor", error.message);
    }
  });
}
if (summarizeTutorBtn) {
  summarizeTutorBtn.addEventListener("click", summarizeLatestTutorAnswer);
}
if (quickSummaryBtn) {
  quickSummaryBtn.addEventListener("click", summarizeLatestTutorAnswer);
}
if (tutorModeButtons.length) {
  tutorModeButtons.forEach((button) => {
    button.addEventListener("click", () => {
      setTutorMode(button.dataset.tutorMode || "calm");
    });
  });
  refreshVideoSearchResults();
}
refreshWeeklyPlanBtn.addEventListener("click", refreshWeeklyPlan);
refreshWeeklyPlanBtnAlt.addEventListener("click", refreshWeeklyPlan);
if (refreshStudyGroupsBtn) {
  refreshStudyGroupsBtn.addEventListener("click", () => {
    if (activeProfile) {
      fetchStudyGroups(activeProfile.name).catch((error) => setAstraStatus(error.message, "warning", true));
    }
  });
}
if (groupMainForm) {
  groupMainForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const content = groupMainInput ? groupMainInput.value.trim() : "";
    if (!content) {
      return;
    }
    if (groupMainInput) {
      groupMainInput.value = "";
    }
    try {
      await sendGroupMainMessage(content, "student");
    } catch (error) {
      setAstraStatus(error.message, "warning", true);
    }
  });
}
if (groupTutorNextBtn) {
  groupTutorNextBtn.addEventListener("click", async () => {
    groupTutorNextBtn.disabled = true;
    try {
      await sendGroupMainMessage("", "tutor");
    } catch (error) {
      setAstraStatus(error.message, "warning", true);
    } finally {
      groupTutorNextBtn.disabled = false;
    }
  });
}
if (groupStepOutBtn) {
  groupStepOutBtn.addEventListener("click", async () => {
    try {
      await stepIntoGroupBreakout();
    } catch (error) {
      setAstraStatus(error.message, "warning", true);
    }
  });
}
if (groupBreakoutForm) {
  groupBreakoutForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const content = groupBreakoutInput ? groupBreakoutInput.value.trim() : "";
    if (!content) {
      return;
    }
    if (groupBreakoutInput) {
      groupBreakoutInput.value = "";
    }
    try {
      await sendGroupBreakoutMessage(content);
    } catch (error) {
      setAstraStatus(error.message, "warning", true);
    }
  });
}
if (groupRejoinBtn) {
  groupRejoinBtn.addEventListener("click", async () => {
    try {
      await rejoinGroupSession();
    } catch (error) {
      setAstraStatus(error.message, "warning", true);
    }
  });
}
if (refreshProgressBtn) {
  refreshProgressBtn.addEventListener("click", () => {
    if (activeProfile) {
      fetchProgress(activeProfile.name);
    }
  });
}
if (progressTrendLensBtn) {
  progressTrendLensBtn.addEventListener("click", async () => {
    if (!activeProfile) {
      return;
    }
    progressTrendLensBtn.disabled = true;
    try {
      await fetchProgress(activeProfile.name);
      if (progressComparisonText) {
        progressComparisonText.scrollIntoView({ block: "nearest", behavior: "smooth" });
      }
    } finally {
      progressTrendLensBtn.disabled = false;
    }
  });
}
if (analyticsDashboardBtn) {
  analyticsDashboardBtn.addEventListener("click", async () => {
    if (!activeProfile) {
      return;
    }
    analyticsDashboardBtn.disabled = true;
    try {
      await loadProgressInsight();
    } finally {
      analyticsDashboardBtn.disabled = false;
    }
  });
}
if (openWeeklyTabBtn) {
  openWeeklyTabBtn.addEventListener("click", () => openPlanSubtab("thisweek"));
}
if (openProgressTabBtn) {
  openProgressTabBtn.addEventListener("click", () => openPlanSubtab("progress"));
}
if (formulasSearchInput) {
  formulasSearchInput.addEventListener("input", () => {
    renderFormulaDetail();
  });
}
if (formulasChapterToggle) {
  formulasChapterToggle.addEventListener("click", () => {
    const isOpen = formulasChapterToggle.getAttribute("aria-expanded") === "true";
    setFormulaChapterDropdown(!isOpen);
  });
}
document.addEventListener("click", (event) => {
  if (!formulasChapterDropdownPanel || !formulasChapterToggle) {
    return;
  }
  const target = event.target;
  if (
    target instanceof Node
    && !formulasChapterDropdownPanel.contains(target)
    && !formulasChapterToggle.contains(target)
  ) {
    closeFormulaChapterDropdown();
  }
});
formulaSubjectButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const subject = normalizeFormulaSubject(button.dataset.formulaSubject);
    if (activeFormulaSubjects.has(subject) && activeFormulaSubjects.size > 1) {
      activeFormulaSubjects.delete(subject);
    } else {
      activeFormulaSubjects.add(subject);
    }
    button.classList.toggle("active", activeFormulaSubjects.has(subject));
    renderFormulaChapterList();
    renderFormulaDetail();
  });
});
if (formulasWeakToggle) {
  formulasWeakToggle.addEventListener("change", async () => {
    if (formulasWeakToggle.checked) {
      await loadFormulaWeakTopics();
    } else {
      setFormulasStatus("");
    }
    renderFormulaChapterList();
    renderFormulaDetail();
  });
}
if (formulasDownloadBtn) {
  formulasDownloadBtn.addEventListener("click", downloadFormulaChapterPdf);
}
  if (generateVideoAnswerBtn) {
    generateVideoAnswerBtn.addEventListener("click", generateVideoAnswerBrief);
  }
if (generateRequestedFullVideoBtn) {
  generateRequestedFullVideoBtn.addEventListener("click", async () => {
    const topic = activeVideoTutorRequest && activeVideoTutorRequest.topic
      ? activeVideoTutorRequest.topic
      : (videoTutorRequestTopicInput && videoTutorRequestTopicInput.value.trim()) || "";
    const subject = activeVideoTutorRequest && activeVideoTutorRequest.subject
      ? activeVideoTutorRequest.subject
      : activeVideoSubjectTab || "";
    if (!topic || !activeVideoTutorBrief) {
      if (videoTutorRequestStatus) {
        videoTutorRequestStatus.textContent = "Prepare the script preview first.";
      }
      return;
    }
    const jobId = await requestTutorVideo(activeVideoTutorBrief.question || topic, topic, subject);
    if (jobId) {
      await updateRequestedVideoStatus(_videoTopicSlug(topic), "generating", jobId, "");
    }
  });
}
if (videoAnswerBtn) {
  videoAnswerBtn.addEventListener("click", () => {
    const question = (videoTutorQuestionInput && videoTutorQuestionInput.value.trim())
      || (lastTutorQuestion || (messageInput && messageInput.value) || lastTutorReply || "").trim();
    const topic = (lastVideoAnswerBrief && lastVideoAnswerBrief.topic) || question;
    const subject = (lastVideoAnswerBrief && lastVideoAnswerBrief.subject) || activeProfile?.exam || "";
    requestTutorVideo(question, topic, subject);
  });
}
speakLastReplyBtn.addEventListener("click", () => {
  const mode = getActiveConversationModeFromUI();
  speakText(lastRepliesByMode[mode] || lastTutorReply || ((activeAvatar && activeAvatar.sample_line) || ""));
});
if (pauseVoiceBtn) {
  pauseVoiceBtn.addEventListener("click", () => {
    pauseTutorNarration();
  });
}
if (resumeVoiceBtn) {
  resumeVoiceBtn.addEventListener("click", async () => {
    await resumeTutorCheckpoint(getActiveConversationModeFromUI());
  });
}
stopVoiceBtn.addEventListener("click", () => {
  interruptTutorOutput(getActiveConversationModeFromUI());
  stopSpeaking();
});
stopLoungeTimerBtn.addEventListener("click", () => {
  clearLoungeTimer();
  updateLoungeTimerLabel();
});
if (loungeVoiceBtn) {
  loungeVoiceBtn.addEventListener("click", toggleLoungeVoiceInput);
}
doubtImageInput.addEventListener("change", async () => {
  try {
    await handleDoubtImageSelection();
  } catch (error) {
    imageUploadStatus.textContent = error.message;
  }
});
analyzeImageBtn.addEventListener("click", analyzeDoubtImage);
saveTutorNameBtn.addEventListener("click", saveTutorName);
addExamBtn.addEventListener("click", addExamPlan);
examCatalogSelect.addEventListener("change", updateExamInputMode);
addPersonBtn.addEventListener("click", addPerson);
addInterestBtn.addEventListener("click", addInterest);
addLifeNoteBtn.addEventListener("click", addLifeNote);
if (uploadSyllabusBtn) {
  uploadSyllabusBtn.addEventListener("click", uploadSyllabusMaterial);
}
languageSelect.addEventListener("change", () => {
  setLanguagePreference(languageSelect.value, { persist: true, updateProfile: true, showConfirmation: true });
});
if (hinglishToggle) {
  hinglishToggle.addEventListener("click", () => {
    const nextLanguage = normalizeLanguageSelection(currentLanguage) === "hinglish" ? "english" : "hinglish";
    setLanguagePreference(nextLanguage, { persist: true, updateProfile: true, showConfirmation: true });
  });
}
if (nightModeToggle) {
  nightModeToggle.addEventListener("change", () => {
    currentTheme = nightModeToggle.checked ? "midnight" : "sunrise";
    applyThemePreferences();
  });
}
if (voiceChatMode) {
  voiceChatMode.addEventListener("change", () => {
    applyAccessibilityPreferences();
    updateTutorRoomLivePanel();
    syncTutorControlStrip();
  });
}
if (tutorVoiceInlineToggleBtn) {
  tutorVoiceInlineToggleBtn.addEventListener("click", () => {
    if (voiceChatMode) {
      voiceChatMode.checked = !voiceChatMode.checked;
      voiceChatMode.dispatchEvent(new Event("change", { bubbles: true }));
    }
  });
}
if (responsePacingSelect) {
  responsePacingSelect.addEventListener("change", () => {
    applyAccessibilityPreferences();
    updateTutorRoomLivePanel();
    syncTutorControlStrip();
  });
}
if (tutorLevelSelect) {
  tutorLevelSelect.addEventListener("change", () => {
    updateTutorLevelHint();
    updateTutorRoomLivePanel();
    syncTutorControlStrip();
  });
}

[highContrastMode, largeTextMode, reducedMotionMode, readingComfortMode, chunkedReplyMode, autoCaptionMode, autoSpeakReplies].forEach((toggle) => {
  if (!toggle) {
    return;
  }
  toggle.addEventListener("change", () => {
    applyAccessibilityPreferences();
    updateTutorRoomLivePanel();
    syncTutorControlStrip();
  });
});
if (showLeagueToggle) {
  showLeagueToggle.addEventListener("change", () => {
    leagueTabVisible = showLeagueToggle.checked;
    applyLeagueVisibility();
  });
}
[showTextExplanation, showVideoExplanation, showVisualExplanation].filter(Boolean).forEach((toggle) => {
  toggle.addEventListener("change", applyExplanationPreferences);
});

personManagerInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    addPerson();
  }
});

interestManagerInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    addInterest();
  }
});

lifeNoteInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    addLifeNote();
  }
});

chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = messageInput.value.trim();
  if (!message) {
    return;
  }
  messageInput.value = "";
  setActiveTab("tutorTab");
  await sendMessage(message);
});

loungeForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = loungeMessageInput.value.trim();
  if (!message) {
    return;
  }
  loungeMessageInput.value = "";
  setActiveTab("loungeTab");
  await sendMessage(message);
});

practiceForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = practiceMessageInput.value.trim();
  if (!message) {
    return;
  }
  lastPracticeMode = "custom practice";
  practiceMessageInput.value = "";
  setActiveTab("practiceTab");
  await sendMessage(message);
});

lastMinuteForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = lastMinuteMessageInput.value.trim();
  if (!message) {
    return;
  }
  lastMinuteMessageInput.value = "";
  setActiveTab("lastMinuteTab");
  await sendMessage(message);
});

guideForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = guideMessageInput.value.trim();
  if (!message) {
    return;
  }
  guideMessageInput.value = "";
  setActiveTab("guideTab");
  await sendMessage(message);
});

tipsForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = tipsMessageInput.value.trim();
  if (!message) {
    return;
  }
  tipsMessageInput.value = "";
  setActiveTab("tipsTab");
  await sendMessage(message);
});

if (startMockTestBtn) {
  startMockTestBtn.addEventListener("click", () => startMockTest());
}
if (mockTestNavPrev) {
  mockTestNavPrev.addEventListener("click", () => goToMockQuestion(-1));
}
if (mockTestNavNext) {
  mockTestNavNext.addEventListener("click", () => goToMockQuestion(1));
}
if (mockTestSubmitBtn) {
  mockTestSubmitBtn.addEventListener("click", finishMockTest);
}
if (mockTestRetakeBtn) {
  mockTestRetakeBtn.addEventListener("click", () => {
    resetMockTestState();
    void loadMockCatalogue();
    void loadMockHistory();
  });
}
if (mockExternalAnalyseBtn) {
  mockExternalAnalyseBtn.addEventListener("click", analyseExternalMock);
}
if (mockTestWeeklyPlanBtn) {
  mockTestWeeklyPlanBtn.addEventListener("click", () => setActiveTab("weeklyTab"));
}
if (mockTestExitBtn) {
  mockTestExitBtn.addEventListener("click", exitMockTestRoom);
}
if (mockTestExitBtnReport) {
  mockTestExitBtnReport.addEventListener("click", exitMockTestRoom);
}
if (mockTestIntegerInput) {
  mockTestIntegerInput.addEventListener("input", () => {
    if (activeMockTest && activeMockTest.questions && activeMockTest.questions[activeMockIndex]) {
      activeMockAnswers[activeMockIndex] = mockTestIntegerInput.value.trim();
    }
  });
}
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && document.body.classList.contains("mock-test-open")) {
    event.preventDefault();
    exitMockTestRoom();
    return;
  }
  if (event.key === "Escape") {
    const hasTutorReply = (lastRepliesByMode.tutor || lastTutorReply || "").trim();
    if (hasTutorReply || activeTutorNarration) {
      event.preventDefault();
      interruptTutorOutput("tutor");
      stopSpeaking();
      updateTutorRoomLivePanel();
    }
  }
});
if (saveProgressItemBtn) {
  saveProgressItemBtn.addEventListener("click", saveProgressItem);
}

[signinEmailInput, signinPasswordInput].forEach((input) => input.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    loadProfile();
  }
}));

[signupName, signupEmail, signupPassword, signupStudentName, signupHours].forEach((input) => {
  input.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      createWebProfile();
    }
  });
});

[customExamNameInput, examDateInput, examSubjectsInput, examPortionInput].forEach((input) => {
  input.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      addExamPlan();
    }
  });
});

if (syllabusTitleInput) {
  syllabusTitleInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      uploadSyllabusMaterial();
    }
  });
}

practiceMessageInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    practiceForm.requestSubmit();
  }
});

[progressExamInput, progressSubjectInput, progressTopicInput, progressNoteInput].filter(Boolean).forEach((input) => {
  input.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      saveProgressItem();
    }
  });
});

lastMinuteMessageInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    lastMinuteForm.requestSubmit();
  }
});

guideMessageInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    guideForm.requestSubmit();
  }
});

tipsMessageInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    tipsForm.requestSubmit();
  }
});

if (enterAstraBtn) {
  enterAstraBtn.addEventListener("click", revealLoginFromSplash);
}

if (skipAstraBtn) {
  skipAstraBtn.addEventListener("click", revealLoginFromSplash);
}

document.addEventListener("keydown", (event) => {
  if (!splashScreen || splashScreen.classList.contains("hidden")) {
    return;
  }
  if (event.key !== "Enter") {
    return;
  }
  const tagName = String(event.target && event.target.tagName ? event.target.tagName : "").toUpperCase();
  if (tagName === "INPUT" || tagName === "TEXTAREA" || tagName === "SELECT" || tagName === "BUTTON") {
    return;
  }
  event.preventDefault();
  revealLoginFromSplash();
});

document.addEventListener("keydown", (event) => {
  if (event.key !== "Escape") {
    return;
  }
  if (tutorConversationDrawer && !tutorConversationDrawer.classList.contains("hidden")) {
    closeTutorConversationDrawer();
  }
});

initializeAstraSplash();
loadAccessibilityPreferences();
loadSidebarPreference();
loadStudioPanePreference();
renderDailyMotivation("");
fetchVideoLibrary().catch((error) => {
  console.warn("Could not load the homepage video library:", error);
  renderAuthHeroVideo(null);
});
refreshTabCollections();
applyTabOrder();
setTutorMode(activeTutorMode);
updateTutorLevelHint();
initLoungeVoiceInput();
setAuthMode("signin");
updateExamInputMode();
applyExplanationPreferences();
renderConceptCanvas(null);

  if (supportsSpeech()) {
    loadBrowserVoices();
    window.speechSynthesis.onvoiceschanged = loadBrowserVoices;
  } else {
    setAvatarStatusText("Browser Voice Unavailable");
    setCaption("Browser speech is unavailable on this device.");
  }






