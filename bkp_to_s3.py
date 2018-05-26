# -*- coding: utf-8 -*-

import time
import subprocess

def main():

    horaInicio             = time.strftime('%H:%M:%S') # Cria hora atual
    pathlog                = geralog()                 # Executa funcao geralog
    dumpfile,backup,upload = gerabackup()              # Executa funcao gerabackup e faz o upload
    log                    = ' >> %s' % pathlog        # Direciona log do backup para o pathlog
    start                  = inicio(horaInicio)        # Executa funcao inicio

    #Printa o Banner
    l = open(pathlog, 'a')
    l.write(start)
    l.close()

    #RODA O BACKUP
    subprocess.call(dumpfile + log, shell=True) # Chama o subprocesso dumpfile
    subprocess.call(backup + log, shell=True)   # Chama o subprocesso backup
    subprocess.call(upload + log, shell=True)   # Chama o subprocesso swiftFile

    #Printa o final e relatório
    diaInicio = (time.strftime("%d-%m-%Y"))
    final     = fim(diaInicio, horaInicio, backup, pathlog)
    r         = open(pathlog, 'a')  # o 'w' abre o arquivo com permissao de escrita, se fosse só pra ler, seria 'r'
    r.write(final)                  # Escreve no arquivo
    r.close()                       # Fecha e salva o arquivo

#Função para gerar um banner com a hora inicial do Backup
def inicio(horaInicio):

    inicio = '''
  =============================================================================================
||                           ____          _____ _  ___    _ _____                             ||
||                          |  _ \   /\   / ____| |/ / |  | |  __ \                            ||
||                          | |_) | /  \ | |    | ' /| |  | | |__) |                           ||
||                          |  _ < / /\ \| |    |  < | |  | |  ___/                            ||
||                          | |_) / ____ \ |____| . \| |__| | |                                ||
||                          |____/_/    \_\_____|_|\_ \____/|_|                                ||
||                                                                                             ||
  =============================================================================================
                                    BACKUP INICIADO AS %s
  =============================================================================================
''' % horaInicio
    return inicio

#Termino do Script
def fim(diaInicio, horaInicio, backup, pathlog):
    hoje = (time.strftime("%d-%m-%Y"))          # Cria data
    horaFinal   = time.strftime('%H:%M:%S')     # Cria hora
    backup = backup.replace('tar -P -cvf ', '') # Renomeia o arquivo, removendo o "tar -P -cvf "
    final = '''
  =============================================================================================
                                    BACKUP FINALIZADO                                         
  =============================================================================================
||                            
||   HORA INICIAL:    %s  -  %s
||   HORA FINAL  :    %s  -  %s
||   LOG FILE    :    %s
||   BAK FILE    :    %s
||
  =============================================================================================
    ''' % (diaInicio, horaInicio, hoje, horaFinal, pathlog, backup)
    return final

#CONSTROI OS LOGS DO SISTEMA - Definir nome do backup e o arquivo de logs que quer criar.
def geralog():
    date        = (time.strftime("%Y-%m-%d"))               # Cria data
    logfile     = '%s-backup.log' % date                    # Cria arquivo de Log
    pathlog     = '/root/scripts/backup/logs/%s' % logfile  # Arquivo de log

    return pathlog

#CONSTROI O ARQUIVO E PATH DE BACKUP E RETORNA
def gerabackup():
    date         = (time.strftime("%Y-%m-%d"))                     # Cria data
    hora         = (time.strftime('%H-%M-%S'))                     # Cria hora
    swiftstorage = 's3://backup_sonar_db'                          # Define endereço ObjectStorage
    backupfile   = '%s_%s-bkp-pgdump.tar.gz' % (date,hora)         # Cria o nome do arquivo de Backup
    pathdestino  = '/root/scripts/backup/destino/%s' % backupfile  # Define destino onde será gravado o Backup
    pathorigem   = '/root/scripts/backup/origem/'                  # Define Pasta que será 'backupeada'

    #dumpfile   = '/opt/rh/postgresql92/root/usr/bin/pg_dump -U sonar > /%s/%s-%s-PGDUMP.sql' % (pathorigem, date, hora) # Gera o dumpfile do banco

    dumpfile = '/bin/touch %s%s_%s-PGTESTE.sql' % (pathorigem, date, hora)                       # Gera arquivo de teste
    backup   = 'tar -P -cvf %s %s%s_%s-PGTESTE.sql' % (pathdestino, pathorigem, date, hora)      # Compacta arquivo de dump
    upload   = '/opt/itau_sysadmintools/s3cmd/bin/s3cmd put %s %s' % (pathdestino, swiftstorage) # Faz upload para o Object Storage   
    
    return dumpfile,backup,upload

#Roda a funcao main no inicio do codigo
main()
