<script setup lang="ts">
import {
  CListGroup,
  CListGroupItem,
  CButton,
  CModal,
  CModalHeader,
  CModalTitle,
  CModalBody,
} from "@coreui/bootstrap-vue";
import type { QueryFunction } from "react-query/types/core";
import { useQuery } from "vue-query";
import { apiGet } from "../api";
import { useUserStore } from "../stores/user";
import NewRuleForm from "../components/NewRuleForm.vue";
import RuleListItem from "../components/RuleListItem.vue";

const userStore = useUserStore();
const route = `/user/${userStore.username}/rules`;
const { isLoading, isError, data, error } = useQuery(
  route,
  apiGet as QueryFunction<string[]>
);
</script>

<script lang="ts">
export default {
  data() {
    return {
      visibleNewRuleModal: false,
    };
  },
};
</script>

<template>
  <span v-if="isLoading">Loading...</span>
  <span v-else-if="isError">Error: {{ error }}</span>
  <template v-else>
    <CListGroup>
      <CListGroupItem
        class="d-flex justify-content-between align-items-center bg-light"
      >
        <span class="fw-bold">{{ data.length }} rules </span>
        <CButton
          color="primary"
          @click="
            () => {
              visibleNewRuleModal = true;
            }
          "
          >Add a new rule</CButton
        >
        <CModal
          :visible="visibleNewRuleModal"
          @close="
            () => {
              visibleNewRuleModal = false;
            }
          "
        >
          <CModalHeader>
            <CModalTitle>Create New Rule</CModalTitle>
          </CModalHeader>
          <CModalBody><NewRuleForm /></CModalBody>
        </CModal>
      </CListGroupItem>
      <RuleListItem v-for="rule in data" :rule="rule"/>
    </CListGroup>
  </template>
</template>
