```mermaid

flowchart TD
    subgraph title[" "]
        direction TB

        main[" main.py\nRun the program"]

        main --> config
        main --> supabase_client
        main --> whatsapp_sender

        config["⚙️ config.py\nLoads .env variables"]
        supabase_client["🗄️ supabase_client.py\nReads contacts from DB"]
        whatsapp_sender["💬 whatsapp_sender.py\nSends via Z-API"]

        supabase_client --> supabase[(" Supabase\nContacts Database")]
        whatsapp_sender --> zapi[" Z-API\nWhatsApp Messaging"]
        config --> env[" .env\nCredentials & URLs"]
    end

    classDef orchestrator fill:#6c5ce7,stroke:#a29bfe,stroke-width:2px,color:#fff,font-weight:bold
    classDef module fill:#00b894,stroke:#55efc4,stroke-width:2px,color:#fff,font-weight:bold
    classDef external fill:#e17055,stroke:#fab1a0,stroke-width:2px,color:#fff,font-weight:bold

    class main orchestrator
    class config,supabase_client,whatsapp_sender module
    class env,supabase,zapi external

    style title fill:transparent,stroke:none
```

## Arquitetura
Cada módulo tem uma única responsabilidade (princípio SRP do SOLID):
- `config.py` não sabe nada de WhatsApp ou Supabase, só lida com variáveis de ambiente
- `supabase_client.py` não sabe nada de envio, só busca dados
- `whatsapp_sender.py` não sabe nada do banco, só envia mensagens
- `main.py` não tem lógica de negócio, só orquestra os outros módulos