# Redragon Mouse Rebind Mac
A script to help fully rebind you ReDragon mouse side buttons

# Mouse Rebind

Uma ferramenta em Python para identificar e reconfigurar dispositivos de mouse USB, enviando comandos personalizados via interface HID (Human Interface Device).

## 🔍 Funcionalidades

- **Identificação de Dispositivos USB**: Localiza todos os dispositivos USB conectados e exibe informações detalhadas (VID, PID, fabricante, etc.)
- **Conversão automática**: Converte valores entre decimal e hexadecimal
- **Interface interativa**: Solicita todas as informações necessárias ao usuário, não há necessidade de editar o código-fonte
- **Controle HID**: Envia comandos de controle personalizados para dispositivos USB

## 📋 Pré-requisitos

- Python 3.6 ou superior
- Bibliotecas: `pyusb` (instalada automaticamente via pip)
- Acesso a dispositivos USB (permissões de administrador ou regras udev no Linux)

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seunome/mouse-rebind.git
cd mouse-rebind
```

### 2. Instale as dependências

Método 1: Usando pip diretamente:
```bash
pip install -r requirements.txt
```

Método 2: Instalação como pacote Python:
```bash
pip install -e .
```

### 3. Permissões (apenas para Linux)

No Linux, por padrão, usuários comuns não têm permissão para acessar dispositivos USB diretamente. Você tem duas opções:

**Opção 1:** Executar os scripts como root (não recomendado para uso regular):
```bash
sudo python3 mouse_finder.py
sudo python3 mouse_rebind.py
```

**Opção 2 (Recomendada):** Configurar regras udev para permitir acesso ao seu dispositivo:

1. Copie o arquivo de regras para o diretório correto:
```bash
sudo cp 99-mouse-rebind.rules /etc/udev/rules.d/
```

2. Edite o arquivo para adicionar os IDs do seu dispositivo:
```bash
sudo nano /etc/udev/rules.d/99-mouse-rebind.rules
```

3. Recarregue as regras:
```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

## 📖 Como usar

### Passo 1: Identifique o seu dispositivo

Execute o script de identificação para localizar o seu mouse:

```bash
python mouse_finder.py
```

Anote o VID (Vendor ID) e PID (Product ID) do seu mouse, você precisará desses valores.

**Exemplo de saída:**
```
=============================================================
DISPOSITIVOS USB ENCONTRADOS
=============================================================

[1] Gaming Mouse - GameTech
    VID: 9639 (0x25A7), PID: 64008 (0xFA08)
    Número de Série: 123456789
------------------------------------------------------------
```

### Passo 2: Configure o seu mouse

Execute o script de rebind e siga as instruções interativas:

```bash
python mouse_rebind.py
```

O script irá:
1. Solicitar o VID e PID do seu mouse
2. Perguntar quais comandos você deseja enviar
3. Enviar os comandos para o dispositivo

**Exemplo de interação:**
```
=============================================================
CONFIGURAÇÃO DE REBIND DE MOUSE USB
=============================================================

Este script envia comandos para configurar seu mouse USB.
Se você não conhece o VID/PID do seu mouse, execute 'mouse_finder.py' primeiro.

------------------------------------------------------------
CONFIGURAÇÃO DO DISPOSITIVO
------------------------------------------------------------
Digite o VID do mouse (decimal ou hex) [9639]: 
Digite o PID do mouse (decimal ou hex) [64008]: 

VID: 9639 (0x25A7)
PID: 64008 (0xFA08)
Digite o número da interface [0]: 
Digite o tipo de relatório (Report Type) [0x0300]: 

Insira o payload como uma sequência de bytes (valores hexadecimais ou decimais).
Por exemplo: 0x01 0x00 0x04 ou 1 0 4
Payload: 0x01 0x00 0x04

------------------------------------------------------------
RESUMO DA CONFIGURAÇÃO
------------------------------------------------------------
VID: 9639 (0x25A7)
PID: 64008 (0xFA08)
Interface: 0
Tipo de Relatório: 768 (0x0300)
Payload: ['0x1', '0x0', '0x4']

Confirmar e enviar comando? (s/n): s

Localizando dispositivo com VID=0x25A7, PID=0xFA08...
Dispositivo encontrado!
Configurando dispositivo...
Enviando comando: ['0x1', '0x0', '0x4']
Comando enviado com sucesso! Bytes transferidos: 3

Comando processado com sucesso!

Programa finalizado.
```

## 🔧 Personalização

O script de rebind aceita diferentes tipos de comandos, dependendo do seu mouse. Aqui estão alguns exemplos comuns:

- **Alterar DPI**: O formato exato depende do fabricante do seu mouse
- **Reprogramar botões**: Defina novas funções para os botões do mouse
- **Configurar iluminação**: Altere cores ou efeitos de iluminação (em mouses RGB)

## 📝 Notas importantes

1. **Compatibilidade**: Nem todos os mouses suportam personalização via USB HID. Em geral, mouses "gamers" e de alta performance têm maior probabilidade de suportar estes comandos.

2. **Protocolo do fabricante**: Cada fabricante tem seu próprio protocolo para controle do dispositivo. Os comandos exatos (payload) variam de acordo com o modelo e marca do mouse.

3. **Backup de configurações**: Sempre anote suas configurações originais antes de fazer alterações, caso precise reverter.

4. **Windows**: Em sistemas Windows, pode ser necessário instalar os drivers WinUSB ou libusb-win32 para que a biblioteca pyusb funcione corretamente.

## 🛠️ Resolução de problemas

### "Dispositivo não encontrado"
- Verifique se o dispositivo está conectado
- Certifique-se de que os valores de VID e PID estão corretos
- No Linux, verifique as permissões (regras udev ou execute como root)

### "Erro ao enviar comando"
- Verifique se o payload está correto para o seu modelo de mouse
- Alguns mouses requerem configurações específicas de interface ou tipo de relatório

### "Permission denied" no Linux
- Configure as regras udev como descrito na seção de instalação
- Alternativamente, execute o script como root (`sudo python mouse_rebind.py`)

### Problemas no Windows
- Instale os drivers libusb para Windows
- Execute o prompt de comando como administrador

### Erros de importação de módulo
- Certifique-se de que a biblioteca pyusb está instalada: `pip install pyusb`

## 📚 Recursos adicionais

- [Documentação da biblioteca PyUSB](https://github.com/pyusb/pyusb)
- [Especificação USB HID](https://www.usb.org/hid)
- [Padrões de dispositivos HID](https://www.usb.org/document-library/device-class-definition-hid-111)

## 📄 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE) - veja o arquivo LICENSE para detalhes.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

1. Faça um Fork do projeto
2. Crie sua Feature Branch (`git checkout -b feature/amazing-feature`)
3. Commit suas mudanças (`git commit -m 'Add some amazing feature'`)
4. Push para a Branch (`git push origin feature/amazing-feature`)
5. Abra um Pull Request
