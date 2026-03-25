restore: 
const { exec } = require('child_process');

function runRestore(file) {
  const command = `gunzip < ${file} | mysql meu_banco`;

  exec(command, (error) => {
    if (error) {
      console.error('Erro no restore:', error.message);
      return;
    }

    console.log('Restore concluído!');
  });
}

module.exports = { runRestore };


backup: 
const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');

const BACKUP_DIR = path.resolve(__dirname, '../../backups');
const LOG_FILE = path.resolve(__dirname, '../../logs/backup.log');

function runBackup() {
  if (!fs.existsSync(BACKUP_DIR)) {
    fs.mkdirSync(BACKUP_DIR, { recursive: true });
  }

  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const file = path.join(BACKUP_DIR, `db-${timestamp}.sql.gz`);

  const command = `mysqldump --single-transaction meu_banco | gzip > ${file}`;

  exec(command, (error) => {
    if (error) {
      fs.appendFileSync(LOG_FILE, `[${new Date()}] ERRO: ${error.message}\n`);
      return;
    }

    fs.appendFileSync(LOG_FILE, `[${new Date()}] Backup OK: ${file}\n`);
    console.log('Backup criado:', file);
  });
}

module.exports = { runBackup };
