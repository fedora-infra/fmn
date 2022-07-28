<template>
    <li class="nav-item">
        <router-link v-bind="$props" class="nav-link"><slot /></router-link>
    </li>
</template>

<script>
import { RouterLink } from 'vue-router'

export default {
  name: 'MainNavLink',
  inheritAttrs: false,

  props: {
    ...RouterLink.props,
  },
}
</script>
