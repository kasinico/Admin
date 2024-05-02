<template>
    <AuthBaseContainer>
        <template slot="header-contents">
            <h1 class="headline">
                Sign In
            </h1>
        </template>
        <AuthLoginForm />
    </AuthBaseContainer>
</template>
{% extends 'partials/base.html' %}
{% load crispy_forms_tags %}

{% load static %}

{% block title %}Add members{% endblock title %}

{% block content %}
<div class="main-content">
    <div class="page-content">
        <!-- start page title -->
        <div class="page-title-box">
            <div class="container-fluid">
                <div class="row align-items-center">
                    <div class="col-sm-6">
                        <div class="page-title">
                            <h4>Register New Boda Crime</h4>
                            <ol class="breadcrumb m-0">
                                <li class="breadcrumb-item"><a href="javascript: void(0);">Home</a></li>
                                <li class="breadcrumb-item"><a href="javascript: void(0);">Crimes</a></li>
                            </ol>
                        </div>
                    </div>

                </div>
            </div>
        </div>
        <p></p>
        <!-- end page title -->
        <template>
            <ContentBody>
                <MilestonesPageHeader>
                    <TabContainer v-model="tab">
                        <TabItem
                            :checked="tab === 'feature'"
                            :is-active="tab === 'feature'"
                            :count="milestonesCount"
                            value="feature"
                            label="Feature Milestones"
                        />
                        <TabItem
                            v-if="!isClientWorkforce"
                            :checked="tab === 'goal'"
                            :is-active="tab === 'goal'"
                            :count="personalMilestonesCount"
                            value="goal"
                            label="Goal Milestones"
                        />
                    </TabContainer>
                </MilestonesPageHeader>
                <MilestonesPageTable />
                <CreateNewMilestoneModal
                    v-if="showCreateNewMilestoneModal || action ==='New Feature Milestone'"
                    status="create"
                    @close="closeMilestoneModal"
                    @create="getNewMilestone"
                />
                <CreateGoalMilestoneModal
                    v-if="showCreateGoalMilestoneModal || action ==='New Goal Milestone'"
                    status="create"
                    @close="closeGoalMilestoneModal"
                    @create="getCreatedPersonalGoal"
                />
            </ContentBody>
        </template>
        
        <script>
            import debounce from 'source/lib/debounce';
            import { mapActions, mapGetters, mapState } from 'vuex';
            import { MousedownOutside } from 'source/directives/MousedownOutside.js';
            import ContentBody from 'source/components/_generics/ContentBody.vue';
            import CreateNewMilestoneModal from 'source/components/employers/milestones/CreateNewMilestoneModal.vue';
            import CreateGoalMilestoneModal from 'source/components/employers/milestones/CreateGoalMilestoneModal.vue';
            import TabContainer from 'source/components/_generics/TabContainer.vue';
            import TabItem from 'source/components/_generics/TabItem.vue';
            import MilestonesPageHeader from 'source/pages/milestones/milestone-page/MilestonesPageHeader.vue';
            import MilestonesPageTable from 'source/pages/milestones/milestone-page/MilestonesPageTable.vue';
            import { MilestonesPageKeys, MilestonesPageEvent } from 'source/pages/milestones/MilestonesKeys';
        
            export default {
                name: 'MilestonesPage',
        
                components: {
                    ContentBody,
                    CreateNewMilestoneModal,
                    CreateGoalMilestoneModal,
                    MilestonesPageHeader,
                    MilestonesPageTable,
                    TabContainer,
                    TabItem
                },
        
                provide() {
                    return {
                        [MilestonesPageKeys.getMilestonesComputedData]: (name) => this[name],
                        [MilestonesPageKeys.getMilestonesPageData]: (name) => this.$data[name],
                    };
                },
        
                eventBusCallbacks: {
                    [MilestonesPageEvent.selectedSortStatus]: 'assignSortStatus',
                    [MilestonesPageEvent.selectedMilestonesStatus]: 'assignMilestoneStatus',
                    [MilestonesPageEvent.showCreateNewMilestoneModal]: 'showNewMilestoneModal',
                    [MilestonesPageEvent.showCreateGoalMilestoneModal]: 'showNewGoalMilestoneModal',
                    [MilestonesPageEvent.goToFeatureMilestoneDetails]: 'goToFeatureMilestoneDetails',
                    [MilestonesPageEvent.goToGoalMilestoneDetails]: 'goToGoalMilestoneDetails',
                    [MilestonesPageEvent.updateMilestoneData]: 'updateMilestoneDataHandler',
                    [MilestonesPageEvent.paginatorHandler]: 'paginatorHandler',
                    [MilestonesPageEvent.fetchMilestones]: 'fecthMilestonesHandler',
        
                    // People Picker
                    'people-picker-selection': 'addPeoplePickerSelection',
                },
        
                directives: {
                    MousedownOutside
                },
        
                data() {
                    return {
                        selectedSortStatus: { pk: 0, name: 'Most Recent' },
                        sortStatuses: [
                            { 'pk': 0, 'name': 'Most Recent' },
                            { 'pk': 1, 'name': 'Least Recent' },
                            { 'pk': 2, 'name': 'Name' },
                            { 'pk': 3, 'name': 'Start Date' },
                            { 'pk': 4, 'name': 'End Date' }
                        ],
                        selectedColumn: { pk: -1, name: 'All columns' },
                        searchQuery: '',
                        leadSearchKey: '',
                        milestones: [],
                        goalMilestones: [],
                        sizePerRequest: 10,
                        milestonesCount: 0,
                        showCreateNewMilestoneModal: false,
                        showCreateGoalMilestoneModal: false,
                        personalMilestonesCount: 0,
                        isFetching: false,
                        isFetchingData: true,
                        statusTypes: [
                            { pk: 0, name: 'Open' },
                            { pk: 1, name: 'Closed' },
                            { pk: 2, name: 'All Statuses' }
                        ],
                        selectedMilestoneLeads: [],
                        selectedMilestoneStatus: {
                            pk: 0, name: 'Open'
                        }
                    };
                },
        
                computed: {
                    ...mapGetters('auth', ['user', 'clientUserPermissions', 'userWorkforcePermissions']),
                    ...mapGetters('boardActions', ['action']),
                    ...mapGetters('campaign', ['getUsersByWorkforce']),
                    ...mapState('workforce', ['selectedWorkforce']),
        
                    isClientWorkforce() {
                        return this.selectedWorkforce?.is_client_workforce;
                    },
        
                    maxPageCount() {
                        //cache sizePerRequest outside of the function to avoid repeated property access.
                        const sizePerRequest = this.sizePerRequest;
                        const max = (this.tab === 'feature') ? (this.milestonesCount / sizePerRequest)
                            : (this.personalMilestonesCount / sizePerRequest);
                        return Math.ceil(max);
                    },
        
        
                    page: {
                        get() {
                            let page = this.$route.query.page;
                            if (!page || page < 1) {
                                page = 1;
                            } else if (page > this.maxPageCount && this.maxPageCount != 0) {
                                page = this.maxPageCount;
                            }
                            return parseInt(page);
                        },
        
                        set(value) {
                            this.$router.replace({
                                query: { ...this.$route.query, page: value },
                                params: { ...this.$route.params }
                            });
                        }
                    },
        
                    tab: {
                        get() {
                            let tab = this.$route.query.tab;
        
                            if (!tab || !['feature', 'goal'].includes(tab)) {
                                tab = 'feature';
                            }
                            return tab;
                        },
        
                        set(value) {
                            this.currentPage = 1;
                            this.$router.replace({
                                ...this.$route,
                                query: { tab: value },
                            });
                        }
                    },
        
                    showPagination() {
                        if ((this.tab === 'feature' && this.milestonesCount > this.sizePerRequest) ||
                            (this.tab === 'goal' && this.personalMilestonesCount > this.sizePerRequest)) {
                            return true;
                        }
                        return false;
                    },
        
                    canAddMilestone() {
                        return this.hasWorkforcePermission || this.user?.user_profile?.permissions.includes('add_milestone')
                            || this.user?.user_profile?.workforce_ids.includes(this.selectedWorkforce?.pk);
                    },
        
                    workforceUsers() {
                        const users = this.getUsersByWorkforce(this.selectedWorkforce?.pk) || [];
        
                        const loggedInUser = {
                            pk: this.user?.user_profile?.pk,
                            full_name: this.user?.user_profile?.full_name,
                            avatar_url: this.user?.user_profile?.avatar_url
                        };
        
                        const filteredUsers = users.filter(user => user.pk !== loggedInUser.pk);
        
                        const filteredAndSortedUsers = filteredUsers
                            .filter(user => user.full_name.toLowerCase().includes(this.leadSearchKey.toLowerCase()))
                            .sort((firstUser, secondUser) => firstUser.full_name.localeCompare(secondUser.full_name));
        
                        if (loggedInUser && loggedInUser.full_name.toLowerCase().includes(this.leadSearchKey.toLowerCase())) {
                            filteredAndSortedUsers.unshift({
                                avatar_url: loggedInUser.avatar_url,
                                pk: loggedInUser.pk,
                                full_name: loggedInUser.full_name
                            });
                        }
        
                        return filteredAndSortedUsers.map(user => ({
                            avatar_url: user.avatar_url,
                            pk: user.pk,
                            full_name: user.full_name
                        }));
                    },
        
                },
        
                watch: {
                    searchQuery: debounce(
                        function handler(val) {
                            if (((val && val.length > 2) || val.length === 0) && this.tab === 'feature') {
                                this.fetchWorkforceMilestones();
                            }
                            if (((val && val.length > 2) || val.length === 0) && this.tab === 'goal') {
                                this.fetchPersonalGoalMilestones();
                            }
                        }, 500),
        
                    page() {
                        if (this.tab === 'feature') {
                            this.fetchWorkforceMilestones();
                        } else {
                            this.fetchPersonalGoalMilestones();
                        }
                    },
        
                    '$route.query.createMilestone': {
                        handler(value) {
                            if (value === true) {
                                this.showCreateNewMilestoneModal = true;
                                this.$router.replace({
                                    query: {
                                        ...this.$route.query,
                                        createMilestone: false,
                                    }
                                }).catch(() => {
                                    console.error('Suppress routing error for createMilestone route');
                                });
                                this.milestoneTabSelector('createMilestone');
                            }
        
                        },
                        immediate: true
                    },
        
                    '$route.query.createGoalMilestone': {
                        handler(value) {
                            if (value === true) {
                                this.showCreateGoalMilestoneModal = true;
                                this.$router.replace({
                                    query: {
                                        ...this.$route.query,
                                        createGoalMilestone: false,
                                    }
                                }).catch(() => {
                                    console.error('Supress routing error for createGoalMilestone route');
                                });
                                this.milestoneTabSelector('createGoalMilestone');
                            }
        
                        },
                        immediate: true
                    },
        
                    '$route.params.workforce_id': {
                        handler: 'fetchWorkforceMilestones'
                    },
        
                    tab() {
                        this.searchQuery = '';
                        this.resetSortFilter();
                    },
                },
        
                async created() {
                    this.$router.replace({
                        ...this.$route,
                        query: { tab: 'feature' },
                    });
                    await this.fetchWorkforceMilestones();
                    await this.fetchPersonalGoalMilestones();
                    this.isFetchingData = false;
        
                    window.addEventListener('resize', this.handleResize);
                    this.handleResize();
                },
        
                destroyed() {
                    window.removeEventListener('resize', this.handleResize);
                },
        
                methods: {
                    ...mapActions('milestone', ['fetchMilestones', 'fetchPersonalMilestone']),
                    ...mapActions('boardActions', ['initiateAction']),
        
                    sortMilestoneLeads(leads) {
                        return leads.sort((a, b) => a.full_name > b.full_name ? 1: -1);
                    },
        
                    showNewMilestoneModal() {
                        this.showCreateNewMilestoneModal = true;
                    },
        
                    showNewGoalMilestoneModal() {
                        this.showCreateGoalMilestoneModal = true;
                    },
        
                    assignSortStatus(item) {
                        this.selectedSortStatus = item;
                    },
        
                    assignMilestoneStatus(item) {
                        this.selectedMilestoneStatus = item;
                    },
        
                    async fetchWorkforceMilestones() {
                        this.isFetching = true;
                        let filters = {
                            top: (this.page - 1) * this.sizePerRequest,
                            size_per_request: this.sizePerRequest,
                            workforce__pk: this.$route.params.workforce_id,
                            is_personal: false,
                        };
        
                        if (this.searchQuery.length) {
                            filters['title__icontains'] = this.searchQuery;
                        }
        
                        if (this.selectedMilestoneLeads.length) {
                            filters['leads__in'] = this.selectedMilestoneLeads.map(a => a.pk).join();
                        }
        
                        let sortKey = this.selectedSortStatus['name'];
                        if (sortKey !== 'Default') {
                            filters['sort_key'] = sortKey;
                        }
                        if (
                            this.selectedMilestoneStatus &&
                            this.selectedMilestoneStatus.name != 'Default') {
                            const status = this.selectedMilestoneStatus.name === 'Open' ? 'Active'
                                : this.selectedMilestoneStatus.name;
                            filters['milestone_status'] = status;
                        }
                        try {
                            let data = await this.fetchMilestones(filters);
                            if (data.objects.length === 0) {
                                this.milestones = null;
                            } else {
                                this.milestones = data.objects;
                            }
                            this.milestonesCount = data.count;
                        } catch (error) {
                            console.error(error);
                        }
                        this.isFetching = false;
                    },
        
                    async fetchPersonalGoalMilestones() {
                        this.isFetching = true;
                        let filters = {
                            top: (this.page - 1) * this.sizePerRequest,
                            size_per_request: this.sizePerRequest,
                            base__workforce_id: this.$route.params.workforce_id
                        };
                        if (this.searchQuery.length) {
                            filters['base__title__icontains'] = this.searchQuery;
                        }
                        let sortKey = this.selectedSortStatus['name'];
                        if (sortKey !== 'Most Recent') {
                            if (sortKey === 'Least Recent') {
                                filters['sort_key'] = 'pk';
                            } else if (sortKey === 'Start Date') {
                                filters['sort_key'] = 'start_date';
                            } else if (sortKey === 'End Date') {
                                filters['sort_key'] = 'end_date';
                            } else if (sortKey === 'Name') {
                                filters['sort_key'] = 'title';
                            }
                        }
                        if (this.selectedMilestoneStatus) {
                            filters['milestone_status'] = this.selectedMilestoneStatus.name;
                        }
        
                        if (this.selectedMilestoneLeads.length) {
                            filters['leads__in'] = this.selectedMilestoneLeads.map(a => a.pk).join();
                        }
        
                        try {
                            let data = await this.fetchPersonalMilestone({ filters, key: 'is-milestone' });
                            if (data.objects.length === 0) {
                                this.goalMilestones = null;
                            } else {
                                this.goalMilestones = data.objects;
                            }
                            this.personalMilestonesCount = data.count;
                        } catch (error) {
                            console.error(error);
                        }
                        this.isFetching = false;
                    },
        
                    paginatorHandler(value) {
                        this.page = value;
                    },
        
                    goToFeatureMilestoneDetails(milestonePk) {
                        this.$router.push({
                            name: 'milestone-details',
                            params: {
                                ...this.$route.params,
                                milestone_id: milestonePk
                            },
                            query: this.$route.query
                        });
                    },
        
                    goToGoalMilestoneDetails(milestone) {
                        const isMilestoneArchived =
                            this.selectedMilestoneStatus.name === 'Archived';
                        this.$router.push({
                            name: 'goal-milestone-details',
                            params: {
                                ...this.$route.params,
                                milestone_id: milestone.base.pk,
                                personal_milestone_id: milestone.pk,
                                is_archived: isMilestoneArchived,
                            },
                            query: this.$route.query
                        });
                    },
        
                    getNewMilestone() {
                        this.showCreateNewMilestoneModal = false;
                        this.fetchWorkforceMilestones();
                    },
        
                    getCreatedPersonalGoal() {
                        this.showCreateGoalMilestoneModal = false;
                        this.fetchPersonalGoalMilestones();
                    },
        
                    milestoneTabSelector(milestonetab) {
                        (milestonetab === 'createMilestone') ? this.tab = 'feature' : this.tab = 'goal';
                    },
        
                    openCreateGoalMilestoneModal() {
                        this.milestoneTabSelector('createGoalMilestone');
                        this.showCreateGoalMilestoneModal = true;
                    },
        
                    closeMilestoneModal() {
                        this.showCreateNewMilestoneModal = false;
                    },
        
                    closeGoalMilestoneModal() {
                        this.showCreateGoalMilestoneModal = false;
                    },
        
                    resetSortFilter() {
                        this.selectedSortStatus = {};
                        this.selectedMilestoneStatus = { pk: 0, name: 'Open' };
                    },
        
                    updateMilestoneDataHandler(value, key, action='') {
                        if (key === 'selectedMilestoneLeads') {
                            const valueIndex = this.$data[key].findIndex(item => item.pk === value.pk);
                            valueIndex === -1
                                ? this.$data[key].push(value)
                                : this.removeSelectedMilestoneLead(this.$data[key][valueIndex]);
                            this.addRemoveMilestoneLeadList(value, action, valueIndex);
                        }
                        else if (key === 'clear') {
                            this.$set(this.$data, 'selectedMilestoneLeads', []);
                            this.$set(this.$data, 'selectedSortStatus', {});
                            this.$set(this.$data, 'selectedMilestoneStatus', {});
                            this.fecthMilestonesHandler();
                        }
                        else
                            this.$data[key] = value;
                    },
        
                    removeSelectedMilestoneLead(lead) {
                        const selectedLeadIndex = this.selectedMilestoneLeads.findIndex(selected => lead.pk === selected.pk);
                        this.selectedMilestoneLeads.splice(selectedLeadIndex, 1);
                    },
        
                    addRemoveMilestoneLeadList(item, action, leadIndex=null) {
                        action === 'remove' ? this.milestoneLeads.splice(leadIndex, 1) : this.milestoneLeads.push(item);
                        this.sortMilestoneLeads(this.milestoneLeads);
                    },
        
                    addPeoplePickerSelection(data, type) {
                        data.map(d => {
                            let item = this.milestoneLeads.filter(
                                lead => lead.pk === d);
                            for (let i=0; i < item.length; i++) {
                                this.updateMilestoneDataHandler(item[i], 'selectedMilestoneLeads', 'remove');
                            }
                        });
                    },
        
                    fecthMilestonesHandler() {
                        if (this.tab === 'feature') {
                            this.fetchWorkforceMilestones();
                        } else if (this.tab === 'goal') {
                            this.fetchPersonalGoalMilestones();
                        }
                    },
        
                    handleResize() {
                        this.windowWidth = window.innerWidth;
                    },
                }
            };
        </script>
        
        <style lang="scss" scoped>
            @import "source/stylesheets/sass/abstract/bpo-variables.scss";
        
            .content-body {
                height: calc(100vh - 40px);
                overflow-y: auto;
        
                @media #{$mobile} {
                    .tab-group {
                        padding-inline: 16px;
                        width: 100vw;
                    }
                }
            }
        </style>
        
        <div class="container-fluid">
            <div class="page-content-wrapper">
                <p></p>
                <form method="POST" class="CrimeForm" enctype="multipart/form-data">
                    {% csrf_token %}


                    <div class="row">
                        <div class="col-12">
                            <div class="card">
                                <div class="card-body">
                                    <h4 class="header-title">Fill in the required Fields</h4>

                                    <div class="row mb-3">
                                        <label for="name" class="col-sm-2 col-form-label">Full
                                            Name</label>
                                        <div class="col-sm-3">
                                            <input class="form-control" type="text" name="name" placeholder="My name"
                                                id="example-text-input" required>
                                        </div>

                                        <label for="crime_type" class="col-sm-2 col-form-label">Road Traffic
                                            crime</label>
                                        <div class="col-sm-5">
                                            <input class="form-control" type="text" name="crime_type" maxlength="35"
                                                placeholder="Overspeeding/ no reflecter" id="example-text-input">
                                        </div>
                                    </div>

                                    <div class="row mb-3">
                                        <label for="license" class="col-sm-2 col-form-label">vehichle Number
                                            Plate</label>
                                        <div class="col-sm-3">
                                            <input class="form-control" type="text" name="license" maxlength = "8"
                                                placeholder="UBC 342L" id="example-text-input">
                                        </div>

                                        <label for="occupation" class="col-sm-2 col-form-label">occupation /
                                            Comapny</label>
                                        <div class="col-sm-5">
                                            <input class="form-control" type="text" name="occupation"
                                                placeholder="Owner" id="example-text-input">
                                        </div>
                                    </div>


                                    <div class="row mb-3">
                                        <label for="stage" class="col-sm-2 col-form-label">Boda
                                            Stage</label>
                                        <div class="col-sm-3">
                                            <input class="form-control" type="text" name="stage" placeholder="Wandegeya"
                                                id="example-text-input">
                                        </div>
                                        <label for="telephone" class="col-sm-2 col-form-label">Telephone</label>
                                        <div class="col-sm-5">
                                            
                                            <input class="form-control" type="tel" name="telephone" maxlength="10" 
                                            pattern="[0-9]*" placeholder="256 555 555" id="example-tel-input">

                                        </div>

                                    </div>





                                    <div class="row mb-3">
                                        <label for="datetime" class="col-sm-2 col-form-label">Date and time</label>
                                        <div class="col-sm-6">
                                            <input class="form-control" name="datetime" type="date" value=""
                                                id="example-datetime-local-input">
                                        </div>
                                    </div>





                                    <div class="row mb-3">
                                        <label for="custody" class="col-sm-2 col-form-label">Select Custody
                                            Option</label>
                                        <div class="col-sm-6">
                                            <select class="form-select" id="custody" name="custody"
                                                aria-label="Default select example">
                                                <option value="Jinja Rd Police" selected>Jinja Rd Police</option>
                                                <option value="Rubaga Div Police">Rubaga Div Police</option>
                                                <option value="Kiira Rd Police">Kiira Rd Police</option>
                                                <option value="Wandegeya div Police">Wandegeya div Police</option>
                                            </select>
                                        </div>
                                    </div>

                                    <button type="submit" class="btn btn-success " value="Submit"
                                        name="Submit">Save</button>
                                    <i class="form-group__bar"></i>

                                </div>
                            </div>

                        </div> <!-- end col -->

                    </div>
                </form>
                <!-- end row -->
                <p></p>

                <!-- end row -->

                <!-- end row -->
            </div>
        </div> <!-- container-fluid -->
    </div>
    <!-- End Page-content -->
    {% endblock content %}
<script>
    // import {mapState} from 'vuex';
    // import AuthBaseContainer from 'source/components/auth/AuthBaseContainer.vue';
    // import AuthLoginForm from 'source/components/auth/AuthLoginForm.vue';
    // import BlankPageMixin from 'source/mixins/BlankPageMixin';

   /*  export default {
        name: 'LoginPage',

        components: {
            AuthBaseContainer,
            AuthLoginForm,
        },

        mixins: [BlankPageMixin],

        computed: {
            ...mapState('auth', ['user']),
        },

        created() {
            if (this.user) {
                this.$router.replace({name: 'dashboard'});
            }
        },
    }; */
</script>

<!-- <style lang="scss" scoped>
    @import 'source/stylesheets/sass/abstract/variables.scss';

    .headline {
        font-size: 20px;
        color: $darkest-gray;
        padding-bottom: 4px;
    }

    .sub-headline {
        color: $dark-gray;
        padding-bottom: 4px 
    }
</style> -->
    <ContentBody>
        <div class="content-sticky">
            <Toolbar>
                <div class="left">
                    <h1 class="p-h1">
                        Client Queries
                    </h1>
                </div>
                <div class="right">
                    <DropdownButton
                        class="status"
                        :label="selectedStatus ? selectedStatus.name : 'Status'"
                    >
                        <DropdownMenu class="block">
                            <ul>
                                <li
                                    v-for="(stats, index) in status"
                                    :key="index"
                                    @click="selectedStatus = stats"
                                >
                                    <p> {{ stats.name }} </p>
                                </li>
                            </ul>
                        </DropdownMenu>
                    </DropdownButton>

                    <div class="filter-wrapper">
                        <DropdownButton
                            class="filter"
                            :label="filterOption"
                        >
                            <DropdownMenu class="block">
                                <ul>
                                    <li
                                        v-for="filter in filterOptions"
                                        :key="filter"
                                        @click="filterOption = filter"
                                    >
                                        <p> {{ filter }} </p>
                                    </li>
                                </ul>
                            </DropdownMenu>
                        </DropdownButton>
                        <SearchBar
                            v-model="searchKey"
                            :placeholder="`Search ${ filterOption }`"
                        />
                    </div>
                </div>
            </Toolbar>
        </div>
        <div class="content-container">
            <EmptyState
                v-if="!queries.length && !isLoading"
                icon="format-columns"
                primary="No Client Queries"
            />
            <LoadingSpinner v-else-if="isLoading" class="large" />
            <Table v-else>
                <thead>
                    <ColumnSorter
                        v-model="nameSort"
                        :sort-status="nameSort"
                        @change-sort="changeSort('nameSort')"
                    >
                        Name
                    </ColumnSorter>
                    <ColumnSorter
                        v-model="emailSort"
                        :sort-status="emailSort"
                        @change-sort="changeSort('emailSort')"
                    >
                        Email
                    </ColumnSorter>
                    <ColumnSorter
                        v-model="titleSort"
                        :sort-status="titleSort"
                        @change-sort="changeSort('titleSort')"
                    >
                        Title
                    </ColumnSorter>
                    <th> Status </th>
                    <ColumnSorter
                        v-model="dateSort"
                        :sort-status="dateSort"
                        @change-sort="changeSort('dateSort')"
                    >
                        Date Submitted
                    </ColumnSorter>
                </thead>
                <tbody>
                    <tr
                        v-for="query in queries"
                        :key="`query-${query.pk}`"
                    >
                        <td>
                            <div class="info">
                                <Avatar size="small" />
                                <p> {{ query.owner.full_name }} </p>
                            </div>
                        </td>
                        <td>
                            <p> {{ query.owner.email }} </p>
                        </td>
                        <td>
                            <p> {{ query.text }} </p>
                        </td>
                        <td>
                            <div class="info status">
                                <i :class="`mdi mdi-${statusIcon(getStatusDisplay(query))}`" />
                                <!-- <p>  </p> -->
                            </div>
                        </td>
                        <td>
                            <BaseTimezone
                                :timestamp="query.when"
                                format="MMM DD, YYYY"
                            />
                        </td>
                    </tr>
                </tbody>
            </Table>
        </div>
        <div v-if="queriesCount > sizePerRequest && !isLoading" class="pagination-wrapper">
            <Pagination
                v-model="page"
                :max-pages="maxPageCount"
                :edge-pages="true"
            />
        </div>
    </ContentBody>
</template>

<script>
    import { mapActions } from 'vuex';
    import debounce from 'source/lib/debounce';

    import Avatar from 'source/components/_generics/Avatar.vue';
    import BaseTimezone from 'source/components/_generics/BaseTimezone.vue';
    import ColumnSorter from 'source/components/_generics/ColumnSorter.vue';
    import ContentBody from 'source/components/_generics/ContentBody.vue';
    import DropdownButton from 'source/components/_generics/DropdownButton.vue';
    import DropdownMenu from 'source/components/_generics/DropdownMenu.vue';
    import EmptyState from 'source/components/_generics/EmptyState.vue';
    import LoadingSpinner from 'source/components/_generics/LoadingSpinner.vue';
    import Pagination from 'source/components/_generics/Pagination.vue';
    import SearchBar from 'source/components/_generics/SearchBar.vue';
    import Table from 'source/components/_generics/Table.vue';
    import Toolbar from 'source/components/_generics/Toolbar.vue';

    export default {
        name: 'ClientQueriesSection',

        components: {
            Avatar,
            BaseTimezone,
            ColumnSorter,
            ContentBody,
            DropdownButton,
            DropdownMenu,
            EmptyState,
            LoadingSpinner,
            Pagination,
            SearchBar,
            Table,
            Toolbar
        },

        data() {
            return {
                dateSort: 'default',
                emailSort: 'default',
                filterOption: 'Name',
                filterOptions: ['Name', 'Title'],
                isLoading: false,
                maxPageCount: 0,
                nameSort: 'default',
                queries: [],
                queriesCount: null,
                searchKey: '',
                selectedStatus: {
                    pk: -1,
                    name: 'All Status'
                },
                sizePerRequest: 10,
                sortKey: '',
                status: [
                    {
                        pk: -1,
                        name: 'All Status',
                    },
                    {
                        pk: 0,
                        name: 'Pending',
                    },
                    {
                        pk: 4,
                        name: 'Awaiting Solutions'
                    },
                    {
                        pk: 1,
                        name: 'Negotiating',
                    },
                    {
                        pk: 2,
                        name: 'Accepted',
                    },
                    {
                        pk: 3,
                        name: 'Rejected'
                    },
                ],
                titleSort: 'default',
            };
        },

        computed: {
            page: {
                get() {
                    return this.validateQueryPage(this.$route.query.page);
                },

                set(value) {
                    this.$router.push({
                        ...this.$route,
                        query: { ...this.$route.query, page: value }
                    });
                }
            },
        },

        watch: {
            page() {
                this.fetchQueries();
            },

            searchKey: debounce(async function() {
                if (this.searchKey.length > 2 || this.searchKey == '') {
                    this.page = 1;
                    this.fetchQueries();
                }
            }, 500),

            selectedStatus() {
                this.page = 1;
                this.fetchQueries();
            },
        },

        created() {
            this.fetchQueries();
        },

        methods: {
            ...mapActions('scalema',['fetchClientQueries']),

            changeSort(label) {
                if (this.$data[label] === 'ascending') {
                    this.$data[label] = 'descending';
                } else if (this.$data[label] === 'descending') {
                    this.$data[label] = 'default';
                } else {
                    this.$data[label] = 'ascending';
                }
                this.sortKey = label;
                this.fetchQueries();
            },

            async fetchQueries() {
                this.isLoading = true;
                let filters = {
                    'top': (this.page - 1) * this.sizePerRequest,
                    'size_per_request': this.sizePerRequest
                };

                if (this.selectedStatus.pk > -1) {
                    filters['status'] = this.selectedStatus.pk;
                } else {
                    if('status' in filters) {
                        delete filters['status'];
                    }
                }

                if (this.sortKey == 'nameSort') {
                    filters['name_sort'] = this.$data[this.sortKey];
                } else if (this.sortKey == 'titleSort') {
                    filters['title_sort'] = this.$data[this.sortKey];
                } else if (this.sortKey == 'dateSort') {
                    filters['date_sort'] = this.$data[this.sortKey];
                } else if (this.sortKey == 'emailSort') {
                    filters['email_sort'] = this.$data[this.sortKey];
                }

                if (this.filterOption == 'Title') {
                    if (this.searchKey) {
                        filters['title_search'] = this.searchKey;
                    }
                } else {
                    if (this.searchKey) {
                        filters['name_search'] = this.searchKey;
                    }
                }

                try {
                    let response = await this.fetchClientQueries(filters);
                    this.queries = response.objects;
                    this.queriesCount = response.total_card_count;
                    this.maxPageCount = response.pages;
                } catch (error) {
                    this.queries = [];
                    this.queriesCount = null;
                    this.maxPageCount = 0;
                }
                this.isLoading = false;
            },

            getStatusDisplay(query) {
                if (query.client_query_proposals.length) {
                    let status = query.client_query_proposals[0].status_display;
                    if (status === 'Pending') {
                        return 'Pending Client Response';
                    } return status;
                } else {
                    return 'Awaiting Solutions';
                }
            },

            statusIcon(status) {
                if (status == 'Accepted') {
                    return 'check-circle-outline c-success';
                }
                else if (status == 'Pending Client Response' || status == 'Negotiating' ||
                    status == 'Awaiting Solutions') {
                    return 'clock-outline c-warning';
                }
                else {
                    return 'close-circle-outline c-error';
                }
            },

            validateQueryPage(query) {
                if (isNaN(parseInt(query)) || parseInt(query) < 1) {
                    return 1;
                } else {
                    return parseInt(query);
                }
            }
        }
    };
</script>

<style lang="scss" scoped>
    @import 'source/stylesheets/sass/abstract/bpo-variables.scss';

    .filter-wrapper {
        display: flex;

            & > * + * {
                margin-left: -1px;
            }
    }

    .content-container {
        margin-top: 32px;

        td {
            &:last-child {
                width: 180px;
            }
        }
        .info {
            display: flex;
            align-items: center;
            gap: 12px;

            i {
                font-size: 16px;
            }
        }
    }

    .pagination-wrapper {
        text-align: center;
    }

</style>
