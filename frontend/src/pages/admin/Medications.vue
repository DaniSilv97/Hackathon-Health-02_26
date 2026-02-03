<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '@/services/api'

const medications = ref([])
const dosageForms = ref([])
const loading = ref(true)
const error = ref(null)
const showModal = ref(false)
const editingMedication = ref(null)
const searchQuery = ref('')

const form = ref({
  name: '',
  description: '',
  dosage_form: 'tablet',
  strength: '',
  manufacturer: '',
  instructions: '',
  side_effects: '',
  is_active: true,
})

const filteredMedications = computed(() => {
  if (!searchQuery.value) return medications.value
  const query = searchQuery.value.toLowerCase()
  return medications.value.filter(m =>
    m.name.toLowerCase().includes(query) ||
    m.manufacturer?.toLowerCase().includes(query)
  )
})

async function fetchMedications() {
  try {
    loading.value = true
    const [medsRes, formsRes] = await Promise.all([
      api.get('/api/medications?active_only=false'),
      api.get('/api/medications/dosage-forms'),
    ])
    medications.value = medsRes.data.medications
    dosageForms.value = formsRes.data.dosage_forms
  } catch (err) {
    error.value = 'Erro ao carregar medicamentos'
    console.error(err)
  } finally {
    loading.value = false
  }
}

function openCreateModal() {
  editingMedication.value = null
  form.value = {
    name: '', description: '', dosage_form: 'tablet', strength: '',
    manufacturer: '', instructions: '', side_effects: '', is_active: true
  }
  showModal.value = true
}

function openEditModal(medication) {
  editingMedication.value = medication
  form.value = { ...medication }
  showModal.value = true
}

async function saveMedication() {
  try {
    if (editingMedication.value) {
      await api.put(`/api/medications/${editingMedication.value.id}`, form.value)
    } else {
      await api.post('/api/medications', form.value)
    }
    showModal.value = false
    await fetchMedications()
  } catch (err) {
    alert(err.response?.data?.error || 'Erro ao guardar')
  }
}

async function toggleActive(medication) {
  try {
    await api.put(`/api/medications/${medication.id}`, {
      is_active: !medication.is_active
    })
    await fetchMedications()
  } catch (err) {
    alert(err.response?.data?.error || 'Erro ao alterar estado')
  }
}

function getFormLabel(value) {
  const form = dosageForms.value.find(f => f[0] === value)
  return form ? form[1] : value
}

onMounted(fetchMedications)
</script>

<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="page-title mb-0">Catalogo de Medicamentos</h1>
      <button @click="openCreateModal" class="btn btn-primary">
        + Novo Medicamento
      </button>
    </div>

    <!-- Search -->
    <div class="card mb-6">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Pesquisar medicamentos..."
        class="input"
      />
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-8">
      <p class="text-gray-500">A carregar...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="card bg-red-50 text-red-700">
      {{ error }}
    </div>

    <!-- Medications Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="med in filteredMedications"
        :key="med.id"
        :class="['card', !med.is_active && 'opacity-60']"
      >
        <div class="flex justify-between items-start mb-2">
          <h3 class="font-semibold text-lg">{{ med.name }}</h3>
          <span
            :class="med.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
            class="px-2 py-1 rounded-full text-xs"
          >
            {{ med.is_active ? 'Ativo' : 'Inativo' }}
          </span>
        </div>

        <div class="text-sm text-gray-600 space-y-1 mb-4">
          <p><strong>Forma:</strong> {{ getFormLabel(med.dosage_form) }}</p>
          <p v-if="med.strength"><strong>Dosagem:</strong> {{ med.strength }}</p>
          <p v-if="med.manufacturer"><strong>Fabricante:</strong> {{ med.manufacturer }}</p>
          <p v-if="med.description" class="text-gray-500 mt-2">{{ med.description }}</p>
        </div>

        <div class="flex justify-end gap-2 pt-2 border-t">
          <button @click="openEditModal(med)" class="text-blue-600 hover:text-blue-800 text-sm">
            Editar
          </button>
          <button
            @click="toggleActive(med)"
            :class="med.is_active ? 'text-red-600 hover:text-red-800' : 'text-green-600 hover:text-green-800'"
            class="text-sm"
          >
            {{ med.is_active ? 'Desativar' : 'Ativar' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-lg max-h-[90vh] overflow-y-auto">
        <h2 class="text-xl font-bold mb-4">
          {{ editingMedication ? 'Editar Medicamento' : 'Novo Medicamento' }}
        </h2>

        <form @submit.prevent="saveMedication" class="space-y-4">
          <div>
            <label class="label">Nome *</label>
            <input v-model="form.name" type="text" required class="input" />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="label">Forma *</label>
              <select v-model="form.dosage_form" class="input">
                <option v-for="[value, label] in dosageForms" :key="value" :value="value">
                  {{ label }}
                </option>
              </select>
            </div>
            <div>
              <label class="label">Dosagem</label>
              <input v-model="form.strength" type="text" class="input" placeholder="ex: 500mg" />
            </div>
          </div>

          <div>
            <label class="label">Fabricante</label>
            <input v-model="form.manufacturer" type="text" class="input" />
          </div>

          <div>
            <label class="label">Descricao</label>
            <textarea v-model="form.description" class="input" rows="2"></textarea>
          </div>

          <div>
            <label class="label">Instrucoes</label>
            <textarea v-model="form.instructions" class="input" rows="2"></textarea>
          </div>

          <div>
            <label class="label">Efeitos Secundarios</label>
            <textarea v-model="form.side_effects" class="input" rows="2"></textarea>
          </div>

          <div class="flex items-center">
            <input v-model="form.is_active" type="checkbox" id="is_active" class="mr-2" />
            <label for="is_active">Ativo</label>
          </div>

          <div class="flex justify-end gap-3 pt-4">
            <button type="button" @click="showModal = false" class="btn btn-secondary">
              Cancelar
            </button>
            <button type="submit" class="btn btn-primary">
              Guardar
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
