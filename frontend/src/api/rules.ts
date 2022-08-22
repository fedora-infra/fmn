import { useUserStore } from "@/stores/user";
import { useMutation } from "vue-query";
import { apiPost } from "./index";
import type { Rule } from "./types";

// Add a new rule
export const useAddRuleMutation = () => {
  const userStore = useUserStore();
  return useMutation<Rule, unknown, Rule>((data) =>
    apiPost(`/user/${userStore.username}/rules`, data)
  );
};
