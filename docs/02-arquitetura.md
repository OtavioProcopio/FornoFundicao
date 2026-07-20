# 🏛️ Arquitetura do Sistema — Ingestão Automática Direct-to-DB (24/7)

## 💡 Princípios de Arquitetura Confirmados

1. **Ingestão 100% Automática (Sem Apontamento Manual)**: Os pirômetros transmitem os dados via rádio para o receptor USB.
2. **Conexão Direta ao Banco (Opção A Exclusiva)**: O software do receptor USB insere diretamente as medições no banco de dados PostgreSQL.
3. **Opções de Hospedagem do Banco (Local vs VPS na Nuvem)**:
   - **Opção Local**: Banco PostgreSQL rodando em um servidor/PC 24/7 na rede interna da fábrica.
   - **Opção VPS (Nuvem - Recomendado)**: Banco PostgreSQL rodando em uma VPS (ex: DigitalOcean, AWS, Hetzner, Linode) com IP público/VPN e criptografia SSL.

---

## ☁️ Como Funciona a Hospedagem em VPS

Se o banco de dados e a API estiverem hospedados em uma VPS na nuvem:

```
 [4 Pirômetros Físicos]
          │ (Rádio)
          ▼
 [PC Host com Receptor USB na Fábrica]
          │
          │ (Internet Segura - SSL/TLS na porta 5432)
          ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ ☁️ VPS na Nuvem (DigitalOcean / AWS / Hetzner / Linode)     │
 │                                                             │
 │   - IP Público / Domínio (ex: db.reiautoparts.com)           │
 │   - PostgreSQL 16 (Porta 5432 com SSL ativo)                │
 │   - API FastAPI (Container Docker em Produção)              │
 └────────┬────────────────────────────────────────────────────┘
          │
          ├──► 📱 Dashboard Acessível de Qualquer Lugar (Casa, Celular, Fábrica)
          └──► 💾 Backups Automáticos 24/7 pela Provedora da VPS
```

---

## 🔒 Requisitos para Conectar o Software da Fábrica à VPS

Para o software do receptor USB gravar direto no banco na VPS:
1. **Credenciais no Software**: No PC da fábrica, configura-se no software:
   * **Host**: IP ou Domínio da VPS (ex: `203.0.113.50` ou `db.reiautoparts.com`).
   * **Porta**: `5432`.
   * **Usuário / Senha / Banco**: Credenciais do PostgreSQL da VPS.
2. **Segurança (Firewall & SSL)**: Liberar no Firewall da VPS o acesso ao PostgreSQL e ativar conexão criptografada (SSL/TLS).
3. **Resiliência a Quedas de Internet**: Caso a internet da fábrica caia temporariamente, a maioria dos softwares de receptores industriais acumula as medições em buffer local e descarrega tudo no banco na VPS assim que a conexão reconecta.
