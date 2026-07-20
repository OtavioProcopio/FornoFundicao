# 🛠️ Guia de Configuração do Receptor USB em Host Local 24/7

Este guia instrui passo a passo como configurar o dispositivo receptor USB dos pirômetros e seu software correspondente em um computador Host local ou Servidor dedicado 24/7 para alimentar automaticamente o banco de dados (seja local ou na VPS).

---

## 📌 Passo 1: Escolha e Preparação do Hardware Host
1. **Computador/Servidor**: Escolha um PC, Mini PC Industrial ou Servidor que permaneça ligado 24 horas por dia, 7 dias por semana.
2. **Nobreak (Nobreak/UPS)**: Conecte o PC Host a um Nobreak para evitar desligamentos e perda de dados durante oscilações ou quedas de energia na fábrica.
3. **Configuração de Energia (BIOS e SO)**:
   * **Na BIOS**: Ative a opção `Restore on AC Power Loss` (para que o computador ligue automaticamente quando a energia retornar após uma queda).
   * **No Sistema Operacional**: Desative completamente o Modo de Suspensão, Hibernação e Desligamento automático de portas USB (`Power Saving` desativado para portas USB).

---

## 🔌 Passo 2: Instalação Física e Driver USB
1. Conecte o dispositivo receptor USB em uma porta USB traseira da máquina.
2. Instale o driver de comunicação fornecido pelo fabricante do pirômetro (geralmente drivers `FTDI` ou `Silicon Labs CP210x` para emulação de porta serial COM).
3. Abra o Gerenciador de Dispositivos (Windows) ou terminal (`ls /dev/ttyUSB*` no Linux) para confirmar qual porta foi atribuída (ex: `COM3` ou `COM4`).

---

## ⚙️ Passo 3: Configuração do Software do Receptor
1. Abra o software gerenciador do receptor USB.
2. Em **Configurações de Comunicação / Dispositivo**:
   * Selecione a porta atribuída no Passo 2 (ex: `COM3`).
   * Teste o sinal de rádio com um pirômetro próximo.
3. Em **Configurações de Banco de Dados / Exportação SQL**:
   * Marque a opção **Habilitar Exportação para Banco de Dados / SQL Direct**.
   * Preencha os campos de conexão com o seu banco (VPS na Nuvem ou Local):
     * **Host/IP**: IP da sua VPS (ex: `198.51.100.25` ou `db.reiautoparts.com`) ou `localhost`.
     * **Porta**: `5432` (porta padrão do PostgreSQL).
     * **Nome do Banco**: `forno_fundicao`.
     * **Usuário**: `forno_user`.
     * **Senha**: `sua_senha_segura`.
   * Clique em **Testar Conexão** e salve as configurações.

---

## 🤖 Passo 4: Configurar Inicialização Automática 24/7 (Serviço)

Para garantir que o software rode continuamente **sem precisar de alguém logado no Windows/Linux**:

### No Windows (Usando NSSM - Non-Sucking Service Manager):
1. Baixe o utilitário leve `nssm.exe`.
2. Abra o prompt de comando como Administrador e execute:
   ```cmd
   nssm install PirometroUSBService "C:\Caminho\Do\Software\Receptor.exe"
   ```
3. O software do receptor passará a rodar como **Serviço do Windows** com `Tipo de Inicialização: Automático`.

### No Linux (Usando Systemd Daemon):
1. Crie o arquivo `/etc/systemd/system/pirometro-usb.service`:
   ```ini
   [Unit]
   Description=Servico Receptor USB Pirometros
   After=network.target

   [Service]
   Type=simple
   ExecStart=/usr/bin/python3 /caminho/do/script_receptor.py
   Restart=always
   RestartSec=5

   [Install]
   WantedBy=multi-user.target
   ```
2. Ative o serviço: `sudo systemctl enable --now pirometro-usb.service`.

---

## 🧪 Passo 5: Teste de Validação Fim-a-Fim
1. Acione um dos pirômetros físicos para realizar uma medição de teste.
2. Verifique se o mostrador do software indica o recebimento do pacote via rádio.
3. Conecte no banco de dados PostgreSQL e rode o comando:
   ```sql
   SELECT * FROM leitura ORDER BY timestamp DESC LIMIT 1;
   ```
4. Confirme se a nova leitura apareceu gravada com sucesso!
