<template>
  <div class="flex h-screen bg-gray-100">
    <!-- Sidebar -->
    <div class="w-64 bg-white shadow-lg">
      <div class="p-6">
        <h1 class="text-2xl font-bold text-gray-800">Sistema de Eventos</h1>
      </div>
      <nav class="mt-6">
        <div class="px-6 py-2">
          <button
            v-for="item in menuItems"
            :key="item.key"
            @click="activeSection = item.key"
            :class="[
              'w-full text-left px-4 py-2 rounded-lg mb-2 transition-colors',
              activeSection === item.key
                ? 'bg-blue-500 text-white'
                : 'text-gray-600 hover:bg-gray-100'
            ]"
          >
            <i :class="item.icon" class="mr-3"></i>
            {{ item.label }}
          </button>
        </div>
      </nav>
    </div>

    <!-- Main Content -->
    <div class="flex-1 overflow-hidden">
      <div class="p-8">
        <!-- Header -->
        <div class="flex justify-between items-center mb-8">
          <h2 class="text-3xl font-bold text-gray-800">
            {{ getCurrentSectionTitle() }}
          </h2>
          <button
            v-if="!isConsultaSection()"
            @click="openCreateModal"
            class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center"
          >
            <i class="fas fa-plus mr-2"></i>
            Adicionar {{ getCurrentSectionTitle() }}
          </button>
          <button
            v-if="isConsultaSection()"
            @click="refreshConsulta"
            class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg flex items-center"
          >
            <i class="fas fa-sync-alt mr-2"></i>
            Atualizar Dados
          </button>
        </div>

        <!-- Content Area -->
        <div class="bg-white rounded-lg shadow overflow-hidden">
          <!-- Eventos Futuros -->
          <div v-if="activeSection === 'eventos-futuros'">
            <div class="p-6 bg-blue-50 border-b">
              <h3 class="text-lg font-semibold text-blue-800 mb-2">Eventos Futuros</h3>
              <p class="text-blue-600">Lista de eventos que ainda não aconteceram, ordenados por preço (maior para menor)</p>
            </div>
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Evento</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data Início</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Local</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Categoria</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Organizador</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Preço</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="evento in eventosFuturos" :key="evento.id_evento" class="hover:bg-gray-50">
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                          <i class="fas fa-calendar-alt text-blue-600"></i>
                        </div>
                        <div class="text-sm font-medium text-gray-900">{{ evento.nome_evento }}</div>
                      </div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatDate(evento.data_inicio) }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ evento.nome_local }}</td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                        {{ evento.nome_categoria }}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ evento.nome_organizador }}</td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span class="text-lg font-bold text-green-600">R$ {{ evento.preco }}</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>


          <div v-if="activeSection === 'media-preco-categoria'">
            <div class="p-6 bg-green-50 border-b">
              <h3 class="text-lg font-semibold text-green-800 mb-2">Média de Preço por Categoria</h3>
              <p class="text-green-600">Análise de preços médios por categoria de eventos já finalizados</p>
            </div>
            <div class="p-6">
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
                <div v-for="categoria in mediaPrecoCategoria" :key="categoria.categoria" class="bg-gradient-to-r from-green-400 to-blue-500 rounded-lg p-6 text-white">
                  <div class="flex items-center justify-between">
                    <div>
                      <h4 class="text-lg font-semibold">{{ categoria.categoria }}</h4>
                      <p class="text-sm opacity-90">{{ categoria.quantidade_eventos }} eventos</p>
                    </div>
                    <div class="text-right">
                      <div class="text-2xl font-bold">R$ {{ categoria.media_preco }}</div>
                      <div class="text-sm opacity-90">Preço médio</div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                  <thead class="bg-gray-50">
                    <tr>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Categoria</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quantidade de Eventos</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Preço Médio</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                    </tr>
                  </thead>
                  <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="categoria in mediaPrecoCategoria" :key="categoria.categoria" class="hover:bg-gray-50">
                      <td class="px-6 py-4 whitespace-nowrap">
                        <div class="flex items-center">
                          <div class="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center mr-3">
                            <i class="fas fa-chart-bar text-purple-600"></i>
                          </div>
                          <div class="text-sm font-medium text-gray-900">{{ categoria.categoria }}</div>
                        </div>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                          {{ categoria.quantidade_eventos }} eventos
                        </span>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <span class="text-lg font-bold text-green-600">R$ {{ categoria.media_preco }}</span>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <span :class="getPriceStatusClass(categoria.media_preco)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                          {{ getPriceStatus(categoria.media_preco) }}
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <div v-if="activeSection === 'eventos-sobrepostos'">
            <div class="p-6 bg-red-50 border-b">
              <h3 class="text-lg font-semibold text-red-800 mb-2">Conflitos de Eventos</h3>
              <p class="text-red-600">Eventos que acontecem no mesmo local com horários sobrepostos</p>
            </div>
            <div v-if="eventosSobrepostos.length === 0" class="p-12 text-center">
              <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <i class="fas fa-check-circle text-green-600 text-2xl"></i>
              </div>
              <h3 class="text-lg font-medium text-gray-900 mb-2">Nenhum Conflito Encontrado!</h3>
              <p class="text-gray-500">Todos os eventos estão bem organizados sem sobreposições de horário.</p>
            </div>
            <div v-else class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Local</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Evento 1</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Horário Evento 1</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Evento 2</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Horário Evento 2</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Severidade</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="conflito in eventosSobrepostos" :key="`${conflito.evento_1}-${conflito.evento_2}`" class="hover:bg-red-50">
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <div class="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center mr-3">
                          <i class="fas fa-exclamation-triangle text-red-600"></i>
                        </div>
                        <div class="text-sm font-medium text-gray-900">{{ conflito.local }}</div>
                      </div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      Evento #{{ conflito.evento_1 }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <div>{{ formatDate(conflito.inicio_1) }}</div>
                      <div class="text-xs text-gray-400">até {{ formatDate(conflito.fim_1) }}</div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      Evento #{{ conflito.evento_2 }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <div>{{ formatDate(conflito.inicio_2) }}</div>
                      <div class="text-xs text-gray-400">até {{ formatDate(conflito.fim_2) }}</div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                        <i class="fas fa-exclamation-circle mr-1"></i>
                        Alto
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>


        </div>

        <!-- Content Area -->
        <div class="bg-white rounded-lg shadow overflow-hidden">
          <!-- Categorias -->
          <div v-if="activeSection === 'categorias'">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nome</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Descrição</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="categoria in categorias" :key="categoria.id">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ categoria.nome }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ categoria.descricao }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button @click="editItem(categoria)" class="text-indigo-600 hover:text-indigo-900 mr-4">Editar</button>
                    <button @click="deleteItem(categoria.id, 'categorias')" class="text-red-600 hover:text-red-900">Excluir</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Eventos -->
          <div v-if="activeSection === 'eventos'">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nome</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data Início</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data Fim</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Preço</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="evento in eventos" :key="evento.id">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ evento.nome }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatDate(evento.data_inicio) }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatDate(evento.data_fim) }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">R$ {{ evento.preco }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button @click="editItem(evento)" class="text-indigo-600 hover:text-indigo-900 mr-4">Editar</button>
                    <button @click="deleteItem(evento.id_evento, 'eventos')" class="text-red-600 hover:text-red-900">Excluir</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Locais -->
          <div v-if="activeSection === 'locais'">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nome</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Endereço</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Capacidade</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="local in locais" :key="local.id">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ local.nome }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ local.endereco }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ local.capacidade }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button @click="editItem(local)" class="text-indigo-600 hover:text-indigo-900 mr-4">Editar</button>
                    <button @click="deleteItem(local.id, 'locais')" class="text-red-600 hover:text-red-900">Excluir</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Organizadores -->
          <div v-if="activeSection === 'organizadores'">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nome</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">CNPJ</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="organizador in organizadores" :key="organizador.id">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ organizador.nome }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ organizador.email }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ organizador.cnpj }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button @click="editItem(organizador)" class="text-indigo-600 hover:text-indigo-900 mr-4">Editar</button>
                    <button @click="deleteItem(organizador.id, 'organizadores')" class="text-red-600 hover:text-red-900">Excluir</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Participantes -->
          <div v-if="activeSection === 'participantes'">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nome</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Telefone</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="participante in participantes" :key="participante.id">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ participante.nome }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ participante.email }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ participante.telefone }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button @click="editItem(participante)" class="text-indigo-600 hover:text-indigo-900 mr-4">Editar</button>
                    <button @click="deleteItem(participante.id, 'participantes')" class="text-red-600 hover:text-red-900">Excluir</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Ingressos -->
          <div v-if="activeSection === 'ingressos'">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Evento</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Participante</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data Compra</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="ingresso in ingressos" :key="ingresso.id">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ getEventoNome(ingresso.id_evento) }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ getParticipanteNome(ingresso.id_participante) }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatDate(ingresso.data_compra) }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button @click="editItem(ingresso)" class="text-indigo-600 hover:text-indigo-900 mr-4">Editar</button>
                    <button @click="deleteItem(ingresso.id, 'ingressos')" class="text-red-600 hover:text-red-900">Excluir</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>


          
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">
            {{ isEditing ? 'Editar' : 'Adicionar' }} {{ getCurrentSectionTitle() }}
          </h3>
          
          <!-- Form Fields -->
          <div class="space-y-4">
            <!-- Categoria Form -->
            <div v-if="activeSection === 'categorias'">
              <input v-model="currentItem.nome" placeholder="Nome" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
              <textarea v-model="currentItem.descricao" placeholder="Descrição" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
            </div>

            <!-- Evento Form -->
            <div v-if="activeSection === 'eventos'">
              <input v-model="currentItem.nome" placeholder="Nome" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-2">
              <textarea v-model="currentItem.descricao" placeholder="Descrição" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-2"></textarea>
              <input v-model="currentItem.data_inicio" type="datetime-local" placeholder="Data Início" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-2">
              <input v-model="currentItem.data_fim" type="datetime-local" placeholder="Data Fim" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-2">
              <select v-model="currentItem.id_local" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-2">
                <option value="">Selecione um Local</option>
                <option v-for="local in locais" :key="local.id" :value="local.id">{{ local.nome }}</option>
              </select>
              <select v-model="currentItem.id_categoria" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-2">
                <option value="">Selecione uma Categoria</option>
                <option v-for="categoria in categorias" :key="categoria.id" :value="categoria.id">{{ categoria.nome }}</option>
              </select>
              <select v-model="currentItem.id_organizador" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-2">
                <option value="">Selecione um Organizador</option>
                <option v-for="organizador in organizadores" :key="organizador.id" :value="organizador.id">{{ organizador.nome }}</option>
              </select>
              <input v-model="currentItem.preco" type="number" step="0.01" placeholder="Preço" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
            </div>

            <!-- Local Form -->
            <div v-if="activeSection === 'locais'">
              <input v-model="currentItem.nome" placeholder="Nome" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-2">
              <input v-model="currentItem.endereco" placeholder="Endereço" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-2">
              <input v-model="currentItem.capacidade" type="number" placeholder="Capacidade" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
            </div>

            <!-- Organizador Form -->
            <div v-if="activeSection === 'organizadores'">
              <input v-model="currentItem.nome" placeholder="Nome" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-2">
              <input v-model="currentItem.email" type="email" placeholder="Email" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-2">
              <input v-model="currentItem.cnpj" placeholder="CNPJ" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
            </div>

            <!-- Participante Form -->
            <div v-if="activeSection === 'participantes'">
              <input v-model="currentItem.nome" placeholder="Nome" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-2">
              <input v-model="currentItem.email" type="email" placeholder="Email" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-2">
              <input v-model="currentItem.telefone" placeholder="Telefone" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
            </div>

            <!-- Ingresso Form -->
            <div v-if="activeSection === 'ingressos'">
              <select v-model="currentItem.id_evento" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-2">
                <option value="">Selecione um Evento</option>
                <option v-for="evento in eventos" :key="evento.id" :value="evento.id">{{ evento.nome }}</option>
              </select>
              <select v-model="currentItem.id_participante" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="">Selecione um Participante</option>
                <option v-for="participante in participantes" :key="participante.id" :value="participante.id">{{ participante.nome }}</option>
              </select>
            </div>
          </div>

          <!-- Modal Actions -->
          <div class="flex justify-end space-x-2 mt-6">
            <button @click="closeModal" class="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400">
              Cancelar
            </button>
            <button @click="saveItem" class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600">
              {{ isEditing ? 'Atualizar' : 'Salvar' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      activeSection: 'eventos',
      showModal: false,
      isEditing: false,
      currentItem: {},
      
      menuItems: [
        { key: 'eventos', label: 'Eventos', icon: 'fas fa-calendar' },
        { key: 'categorias', label: 'Categorias', icon: 'fas fa-tags' },
        { key: 'locais', label: 'Locais', icon: 'fas fa-map-marker-alt' },
        { key: 'organizadores', label: 'Organizadores', icon: 'fas fa-users' },
        { key: 'participantes', label: 'Participantes', icon: 'fas fa-user-friends' },
        { key: 'ingressos', label: 'Ingressos', icon: 'fas fa-ticket-alt' },
        { key: 'eventos-futuros', label: 'Eventos Futuros', icon: 'fas fa-clock' },
        { key: 'media-preco-categoria', label: 'Análise de Preços', icon: 'fas fa-chart-bar' },
        { key: 'eventos-sobrepostos', label: 'Conflitos de Eventos', icon: 'fas fa-exclamation-triangle' }
      ],

      eventosFuturos: [],
      mediaPrecoCategoria:[],
      categorias: [],
      eventosSobrepostos: [],
      eventos: [
        
      ],
      
      locais: [
  
      ],
      
      organizadores: [
       
      ],
      
      participantes: [
        
      ],
      
      ingressos: [
        
      ]
    }
  },

  methods: {
    getCurrentSectionTitle() {
      const item = this.menuItems.find(item => item.key === this.activeSection)
      return item ? item.label : ''
    },
    isConsultaSection() {
      return ['eventos-futuros','media-preco-categoria','eventos-sobrepostos'].includes(this.activeSection)
    },
    async refreshConsulta() {
      try {
        if (this.activeSection === 'eventos-futuros') {
          await this.loadEventosFuturos()
        } else if (this.activeSection === 'media-preco-categoria') {
          await this.loadMediaPrecoCategoria()}
        else if (this.activeSection === 'eventos-sobrepostos') {
          await this.loadEventosSobrepostos()
        }
      } catch (error) {
        console.error('Erro ao atualizar consulta:', error)
        alert('Erro ao atualizar dados')
      }
    },


    async loadEventosFuturos() {
      
      const response = await fetch('http://127.0.0.1:5000/eventos/futuros')
      if (response.ok) {
        this.eventosFuturos = await response.json()
      }
    },
    async loadMediaPrecoCategoria() {
    const response = await fetch('http://127.0.0.1:5000/eventos/media-preco-categoria')
    if (response.ok) {
      this.mediaPrecoCategoria = await response.json()
      console.log('Dados recebidos:', this.mediaPrecoCategoria)
    }
},

    async loadEventosSobrepostos() {
          // Substitua pela chamada para sua API
          const response = await fetch('http://127.0.0.1:5000/eventos/sobrepostos')
          if (response.ok) {
            this.eventosSobrepostos = await response.json()
          }
        },  
    getPriceStatus(preco) {
          if (preco >= 150) return 'Premium'
          if (preco >= 100) return 'Médio'
          return 'Econômico'
        },

      getPriceStatusClass(preco) {
          if (preco >= 150) return 'bg-purple-100 text-purple-800'
          if (preco >= 100) return 'bg-yellow-100 text-yellow-800'
          return 'bg-green-100 text-green-800'
        },

    openCreateModal() {
      this.isEditing = false
      this.currentItem = {}
      this.showModal = true
    },

    editItem(item) {
      this.isEditing = true
      this.currentItem = { ...item }
      this.showModal = true
    },

    closeModal() {
      this.showModal = false
      this.currentItem = {}
    },

    async saveItem() {
      try {
        if (this.isEditing) {
          // Atualizar item existente
          await this.updateItem()
        } else {
          // Criar novo item
          await this.createItem()
        }
        this.closeModal()
        this.loadData(this.activeSection)
      } catch (error) {
        console.error('Erro ao salvar:', error)
        alert('Erro ao salvar item')
      }
    },

    async createItem() {
      // Substitua pela chamada para sua API
      const response = await fetch(`http://127.0.0.1:5000/${this.activeSection}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.currentItem)
      })
      
      if (!response.ok) {
        throw new Error('Erro ao criar item')
      }
    },

    async updateItem() {

      let id = '';

      if (this.activeSection == 'eventos') {
        id = this.currentItem.id_evento;
      }

      if (this.activeSection == 'categorias') {
        id = this.currentItem.id_categoria;
      }

      // Substitua pela chamada para sua API
      const response = await fetch(`http://127.0.0.1:5000/${this.activeSection}/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.currentItem)
      })
      
      if (!response.ok) {
        throw new Error('Erro ao atualizar item')
      }
    },

    async deleteItem(id, section) {
      if (confirm('Tem certeza que deseja excluir este item?')) {
        try {
          // Substitua pela chamada para sua API
          const response = await fetch(`http://127.0.0.1:5000/${section}/${id}`, {
            method: 'DELETE'
          })
          
          if (!response.ok) {
            throw new Error('Erro ao excluir item')
          }
          
          this.loadData(section)
        } catch (error) {
          console.error('Erro ao excluir:', error)
          alert('Erro ao excluir item')
        }
      }
    },

    async loadData(section) {
      try {
        let url = `http://127.0.0.1:5000/${section}`;

        // Ajuste para rotas específicas
        if (section === 'media-preco-categoria') {
          url = 'http://127.0.0.1:5000/eventos/media-preco-categoria';
        } else if (section === 'eventos-futuros') {
          url = 'http://127.0.0.1:5000/eventos/futuros';
        }
        
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`Erro na requisição: ${response.status}`);
        }
        const data = await response.json();

        // Atualiza a propriedade correta no Vue
        this[section] = data;
      } catch (error) {
        console.error('Erro ao carregar dados:', error);
      }
    },


    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('pt-BR') + ' ' + date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
    },

    getEventoNome(id) {
      const evento = this.eventos.find(e => e.id === id)
      return evento ? evento.nome : 'N/A'
    },

    getParticipanteNome(id) {
      const participante = this.participantes.find(p => p.id === id)
      return participante ? participante.nome : 'N/A'
    }
  },
  mounted() {
    this.loadData('eventos')
  },

  watch: {
  activeSection(newValue) {
    if (newValue === 'eventos-futuros') {
      this.loadEventosFuturos()
    } else if (newValue === 'media-preco-categoria') {
      this.loadMediaPrecoCategoria()
    } else {
      this.loadData(newValue)  
    }
  }
}


}
</script>

<style>
/* Adicione Font Awesome para os ícones */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');
@import "tailwindcss";

/* Estilos customizados se necessário */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>