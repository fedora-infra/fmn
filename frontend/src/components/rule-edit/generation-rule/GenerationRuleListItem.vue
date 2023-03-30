<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import type { GenerationRule } from "@/api/types";
import { CButton, CButtonGroup, CListGroupItem } from "@coreui/bootstrap-vue";
import { cilPen, cilTrash } from "@coreui/icons";
import { CIcon } from "@coreui/icons-vue";
import DestinationTag from "../../DestinationTag.vue";

const props = defineProps<{
  rule: GenerationRule;
}>();

const emit = defineEmits<{
  (e: "edit"): void;
  (e: "delete"): void;
}>();

const handleEditClicked = () => {
  emit("edit");
};
const handleDeleteClicked = () => {
  emit("delete");
};
</script>

<template>
  <CListGroupItem class="d-flex align-items-center">
    <div>
      <DestinationTag
        :destination="dest"
        :icononly="false"
        v-for="dest in props.rule.destinations"
        :key="`${dest.protocol}:${dest.address}`"
      />
      <div>
        <template
          v-for="(f_params, f_name) in props.rule.filters"
          :key="f_name"
        >
          <span
            class="badge bg-light border border-info text-secondary fw-normal me-1"
            v-if="
              !!f_params && !(Array.isArray(f_params) && f_params.length === 0)
            "
            ><strong>{{ f_name }}</strong>
            <template v-if="typeof f_params !== 'boolean'"> : </template>
            <template v-if="Array.isArray(f_params)">{{
              f_params.join(", ")
            }}</template
            ><template v-else-if="typeof f_params !== 'boolean'">{{
              f_params
            }}</template></span
          >
        </template>
      </div>
    </div>
    <div class="ms-auto">
      <CButtonGroup>
        <CButton
          @click.prevent="handleEditClicked"
          color="primary"
          variant="outline"
        >
          <CIcon :icon="cilPen" />
        </CButton>
        <CButton
          @click.prevent="handleDeleteClicked"
          color="danger"
          variant="outline"
        >
          <CIcon :icon="cilTrash" />
        </CButton>
      </CButtonGroup>
    </div>
  </CListGroupItem>
</template>
