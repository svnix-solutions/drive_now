<template>
  <div class="space-y-2">
    <label v-if="label" class="block text-sm font-medium text-gray-700">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    
    <!-- Regular Input -->
    <Input
      v-if="type !== 'select' && type !== 'textarea'"
      :type="type"
      :placeholder="placeholder"
      :required="required"
      :disabled="disabled"
      :min="min"
      :max="max"
      :rows="rows"
      :modelValue="modelValue"
      @update:modelValue="$emit('update:modelValue', $event)"
      @change="$emit('change', $event)"
      @input="$emit('input', $event)"
      @focus="$emit('focus', $event)"
      @blur="$emit('blur', $event)"
      v-bind="$attrs"
    />
    
    <!-- Textarea -->
    <textarea
      v-else-if="type === 'textarea'"
      :placeholder="placeholder"
      :required="required"
      :disabled="disabled"
      :rows="rows || 3"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      @change="$emit('change', $event)"
      @focus="$emit('focus', $event)"
      @blur="$emit('blur', $event)"
      class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
      v-bind="$attrs"
    />
    
    <!-- Select -->
    <select
      v-else-if="type === 'select'"
      :required="required"
      :disabled="disabled"
      :value="modelValue"
      @change="$emit('update:modelValue', $event.target.value); $emit('change', $event)"
      @focus="$emit('focus', $event)"
      @blur="$emit('blur', $event)"
      class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
      v-bind="$attrs"
    >
      <option v-if="placeholder" value="" disabled>{{ placeholder }}</option>
      <option
        v-for="option in options"
        :key="option.value"
        :value="option.value"
      >
        {{ option.label }}
      </option>
    </select>
  </div>
</template>

<script>
export default {
  name: 'FormControl',
  emits: ['update:modelValue', 'change', 'input', 'focus', 'blur'],
  props: {
    label: String,
    type: {
      type: String,
      default: 'text'
    },
    placeholder: String,
    required: Boolean,
    disabled: Boolean,
    min: [String, Number],
    max: [String, Number],
    rows: Number,
    modelValue: [String, Number],
    options: {
      type: Array,
      default: () => []
    }
  }
}
</script>