<script setup lang="ts">
import { apiPost } from "@/api";
import type { PostError } from "@/api/types";
import { CButton } from "@coreui/bootstrap-vue";
import { FormKit, setErrors } from "@formkit/vue";
import type { AxiosError } from "axios";
import { useMutation } from "vue-query";
import { useRouter } from "vue-router";
import { useUserStore } from "../stores/user";
import DestinationList from "./DestinationList.vue";
import FilterList from "./FilterList.vue";
import TrackingRuleList from "./TrackingRuleList.vue";

const userStore = useUserStore();
const router = useRouter();
/* eslint-disable */
// warning  'isLoading' is assigned a value but never used  @typescript-eslint/no-unused-vars
// warning  'error' is assigned a value but never used      @typescript-eslint/no-unused-vars
// warning  'isError' is assigned a value but never used    @typescript-eslint/no-unused-vars
// warning  'isSuccess' is assigned a value but never used  @typescript-eslint/no-unused-vars
// warning  'data' is defined but never used                @typescript-eslint/no-unused-vars
// warning  'variables' is defined but never used           @typescript-eslint/no-unused-vars
// warning  'context' is defined but never used             @typescript-eslint/no-unused-vars
// warning  'variables' is defined but never used           @typescript-eslint/no-unused-vars
// warning  'context' is defined but never used             @typescript-eslint/no-unused-vars
const { isLoading, error, isError, isSuccess, mutateAsync } = useMutation(
  apiPost,
  {
    onSuccess: (data, variables, context) => {
      // TODO: Add flash / snackbar message
      router.push("/rules");
    },
    onError: (data: AxiosError<PostError>, variables, context) => {
      console.log(data);
      if (!data.response) {
        return;
      }
      setErrors(
        "new-rule",
        data.response.data.detail.map(
          (e) => `Server error: ${e.loc.at(-1)}: ${e.msg}`
        )
      );
    },
  }
);
/* eslint-enable */

/* eslint-disable */
// warning  Unexpected any. Specify a different type  @typescript-eslint/no-explicit-any
const handleSubmit = async (val: any) => {
  console.log("Will submit the new rule:", val);
  await mutateAsync({ url: `/user/${userStore.username}/rules`, data: val });
};
/* eslint-enable */
</script>

<template>
  <FormKit type="form" id="new-rule" @submit="handleSubmit" :actions="false">
    <div class="mb-3">
      <FormKit
        name="name"
        type="text"
        placeholder="Rule name"
        help="Choose a name for your new Rule"
        validation="required"
      />
    </div>
    <div class="mb-3">
      <TrackingRuleList />
    </div>

    <div class="mb-3">
      <DestinationList />
    </div>

    <div class="mb-3">
      <h4>Choose a filter (optional)</h4>
      <FilterList />
    </div>

    <div class="my-3">
      <CButton type="submit" color="primary">Create Rule</CButton>
    </div>
  </FormKit>
</template>
