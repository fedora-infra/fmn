<script setup lang="ts">
import { useAddRuleMutation } from "@/api/rules";
import type { PostError, Rule } from "@/api/types";
import { useToastStore } from "@/stores/toast";
import type { FormKitNode } from "@formkit/core";
import { FormKit } from "@formkit/vue";
import {
  CAccordion,
  CAccordionBody,
  CAccordionHeader,
  CAccordionItem,
} from "@coreui/bootstrap-vue";
import type { AxiosError } from "axios";
import { useRouter } from "vue-router";
import DestinationList from "./DestinationList.vue";
import FilterList from "./FilterList.vue";
import TrackingRuleList from "./TrackingRuleList.vue";

const toastStore = useToastStore();
const router = useRouter();

const { mutateAsync } = useAddRuleMutation();

const handleSubmit = async (data: Rule, form: FormKitNode | undefined) => {
  console.log("Will submit the new rule:", data);
  if (!form) {
    throw Error("No form node?");
  }
  try {
    const response = await mutateAsync(data);
    // Success!
    toastStore.addToast({
      color: "success",
      title: "Rule created",
      content: `Rule "${response.name}" has been successfully created.`,
    });
    router.push("/rules");
  } catch (err) {
    const error = err as AxiosError<PostError>;
    console.log("Got error response from server:", error);
    if (!error.response) {
      return;
    }
    form.setErrors(
      error.response.data.detail.map(
        (e) => `Server error: ${e.loc.at(-1)}: ${e.msg}`
      )
    );
  }
};
const additional_filters_accordion_vars = {
  "--bs-accordion-btn-padding-x": 0,
  "--bs-accordion-btn-padding-y": 0,
  "--bs-accordion-bg": "transparent",
  "--bs-accordion-btn-focus-box-shadow": "none",
  "--bs-accordion-btn-focus-border-color": "none",
};
</script>

<template>
  <FormKit
    type="form"
    id="new-rule"
    @submit="handleSubmit"
    submit-label="Create Rule"
    :submit-attrs="{ class: ['btn', 'btn-primary'] }"
  >
    <div class="mb-4">
      <h4>Choose what you want to track</h4>
      <TrackingRuleList />
    </div>

    <CAccordion flush :style="additional_filters_accordion_vars">
      <CAccordionItem :item-key="1">
        <CAccordionHeader class="align-items-center">
          <h4>Additional Filters</h4>
        </CAccordionHeader>
        <CAccordionBody class="bg-light">
          <FilterList />
        </CAccordionBody>
      </CAccordionItem>
    </CAccordion>

    <div class="mb-4 mt-4">
      <FormKit
        name="name"
        type="text"
        placeholder="Rule name"
        help="Choose a name for your new Rule"
        validation="required"
      />
    </div>
    <div class="mb-4">
      <h4>Choose where you want the notifications to go</h4>
      <DestinationList />
    </div>
  </FormKit>
</template>
