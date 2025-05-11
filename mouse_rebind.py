#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import usb.core
import usb.util
import sys
import time

def decimal_to_hex(decimal_value):
    """Converte um valor decimal para hexadecimal, formatado adequadamente."""
    return f"0x{decimal_value:04X}"

def get_user_input(prompt, default=None, is_int=False):
    """Obtém entrada do usuário com valor padrão opcional."""
    if default is not None:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
        
    while True:
        user_input = input(prompt).strip()
        
        if not user_input and default is not None:
            return default
            
        if is_int:
            try:
                return int(user_input, 0)  # Aceita decimal (123) ou hex (0x7B)
            except ValueError:
                print("Erro: Por favor, insira um número válido (decimal ou hexadecimal).")
        else:
            return user_input

def send_command_to_mouse(vid, pid, payload, interface=0, report_type=0x0300):
    """
    Envia um comando de controle para o mouse.
    
    Args:
        vid: Vendor ID do dispositivo
        pid: Product ID do dispositivo
        payload: Lista de bytes para enviar
        interface: Número da interface (padrão 0)
        report_type: Tipo de relatório (padrão 0x0300)
    
    Returns:
        bool: True se o comando foi enviado com sucesso, False caso contrário
    """
    try:
        # Localiza o dispositivo
        print(f"\nLocalizando dispositivo com VID={decimal_to_hex(vid)}, PID={decimal_to_hex(pid)}...")
        dev = usb.core.find(idVendor=vid, idProduct=pid)
        
        if dev is None:
            print(f"Erro: Dispositivo com VID={decimal_to_hex(vid)}, PID={decimal_to_hex(pid)} não encontrado!")
            return False
            
        print(f"Dispositivo encontrado!")
        
        # Detach do kernel se necessário (Linux)
        try:
            for i in range(3):  # Tenta em múltiplas interfaces
                if dev.is_kernel_driver_active(i):
                    print(f"Liberando driver do kernel na interface {i}...")
                    dev.detach_kernel_driver(i)
        except Exception as e:
            print(f"Aviso ao liberar driver: {e}")
        
        # Configura o dispositivo
        print("Configurando dispositivo...")
        try:
            dev.set_configuration()
        except Exception as e:
            print(f"Aviso na configuração: {e}")
            print("Tentando continuar mesmo assim...")
        
        # Envia o comando de controle
        print(f"Enviando comando: {[hex(x) for x in payload]}")
        result = dev.ctrl_transfer(
            0x21,      # Tipo de requisição (Class | Interface)
            0x09,      # SET_REPORT
            report_type,
            interface,
            payload,
            timeout=1000
        )
        
        print(f"Comando enviado com sucesso! Bytes transferidos: {result}")
        return True
        
    except usb.core.USBError as e:
        print(f"Erro USB ao enviar comando: {e}")
        return False
    except Exception as e:
        print(f"Erro geral ao enviar comando: {e}")
        return False

def get_payload_from_user():
    """Solicita ao usuário que insira a sequência de bytes para o payload."""
    print("\nInsira o payload como uma sequência de bytes (valores hexadecimais ou decimais).")
    print("Por exemplo: 0x01 0x00 0x04 ou 1 0 4")
    
    payload_str = input("Payload: ")
    payload_parts = payload_str.split()
    
    payload = []
    for part in payload_parts:
        try:
            # Converte a string para um inteiro (decimal ou hex)
            byte_value = int(part, 0)
            if 0 <= byte_value <= 255:
                payload.append(byte_value)
            else:
                print(f"Aviso: Valor {part} fora do intervalo válido para um byte (0-255), usando 0.")
                payload.append(0)
        except ValueError:
            print(f"Aviso: Valor inválido '{part}', usando 0 no lugar.")
            payload.append(0)
    
    if not payload:
        print("Payload vazio, usando valores padrão [0x01, 0x00, 0x04]")
        return [0x01, 0x00, 0x04]
        
    return payload

def interactive_mode():
    """Interface interativa para configurar e enviar comandos para o mouse."""
    print("\n" + "=" * 60)
    print("CONFIGURAÇÃO DE REBIND DE MOUSE USB")
    print("=" * 60)
    
    print("\nEste script envia comandos para configurar seu mouse USB.")
    print("Se você não conhece o VID/PID do seu mouse, execute 'mouse_finder.py' primeiro.")
    
    print("\n" + "-" * 60)
    print("CONFIGURAÇÃO DO DISPOSITIVO")
    print("-" * 60)
    
    # Obtém informações do dispositivo
    vid = get_user_input("Digite o VID do mouse (decimal ou hex)", default=0x25A7, is_int=True)
    pid = get_user_input("Digite o PID do mouse (decimal ou hex)", default=0xFA08, is_int=True)
    
    print(f"\nVID: {vid} ({decimal_to_hex(vid)})")
    print(f"PID: {pid} ({decimal_to_hex(pid)})")
    
    # Obtém parâmetros avançados
    interface = get_user_input("Digite o número da interface", default=0, is_int=True)
    
    report_type_default = 0x0300
    report_type = get_user_input(
        "Digite o tipo de relatório (Report Type)",
        default=f"0x{report_type_default:04X}",
        is_int=True
    )
    
    # Obtém payload
    payload = get_payload_from_user()
    
    # Confirmação
    print("\n" + "-" * 60)
    print("RESUMO DA CONFIGURAÇÃO")
    print("-" * 60)
    print(f"VID: {vid} ({decimal_to_hex(vid)})")
    print(f"PID: {pid} ({decimal_to_hex(pid)})")
    print(f"Interface: {interface}")
    print(f"Tipo de Relatório: {report_type} ({decimal_to_hex(report_type)})")
    print(f"Payload: {[hex(x) for x in payload]}")
    
    confirm = input("\nConfirmar e enviar comando? (s/n): ").strip().lower()
    if confirm != 's':
        print("Operação cancelada pelo usuário.")
        return
    
    # Envia o comando
    if send_command_to_mouse(vid, pid, payload, interface, report_type):
        print("\nComando processado com sucesso!")
    else:
        print("\nFalha ao processar o comando. Verifique o dispositivo e as permissões.")

def main():
    try:
        interactive_mode()
    except KeyboardInterrupt:
        print("\n\nOperação interrompida pelo usuário.")
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        
    print("\nPrograma finalizado.")

if __name__ == "__main__":
    main()
