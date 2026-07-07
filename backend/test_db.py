from db import inserir_senha, proxima_senha

# Emitir gerais
print(inserir_senha("G"))  # G001
print(inserir_senha("G"))  # G002
print(inserir_senha("G"))  # G003
print(inserir_senha("G"))  # G004

# Emitir prioridade
print(inserir_senha("P"))  # P001

# Emitir mais uma geral
print(inserir_senha("G"))  # G005

# Ver próxima senha
print("Próxima senha:", proxima_senha())

