<template>
  <div
      @dragenter.prevent="toggleActive"
      @dragleave.prevent="toggleActive"
      @dragover.prevent
      @drop.prevent="toggleActive"
      :class="{'active-dropzone': active}"
      class="dropzone">
    <span>Drag or Drop File</span>
    <span>OR</span>
    <label for="dropzoneFile">Select File</label>
    <input type="file" id="dropzoneFile">
  </div>
</template>

<script>
import {ref} from "vue";

export default {
  name: "DropZone",
  setup() {
    const active = ref(false);

    const toggleActive = () => {
      active.value = !active.value;
    }

    return { active, toggleActive }
  }
}
</script>

<style scoped>
.dropzone {
  width: 400px;
  height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  row-gap: 16px;
  border: 2px dashed #266ac3;
  background-color: #fff;
  transition: .3s ease all;
}

.dropzone label {
  padding: 8px 12px;
  color: #fff;
  background-color: #266ac3;
  cursor: pointer;
  transition: .3s ease all;
}

.dropzone label:hover {
  background-color: #1c4f92;
}

.dropzone input {
  display: none;
}

.active-dropzone {
  background-color: #266ac3;
  color: #fff;
  border: 2px dashed #fff;
}

.active-dropzone label {
  background-color: #fff;
  color: #266ac3;
}

</style>