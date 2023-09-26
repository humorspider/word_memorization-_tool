import random

class Player:
    def __init__(self):
        self.name = "Player"
        self.level = 1
        self.health = 100
        self.attack = 10
        self.defense = 5
    
    def attack_enemy(self, enemy):
        damage = self.attack + random.randint(1, 5)
        enemy.take_damage(damage)
        
    def take_damage(self, damage):
        defense_effect = random.randint(1, 3) * self.defense
        actual_damage = max(0, damage - defense_effect)
        self.health -= actual_damage
        if self.health <= 0:
            print("Game Over")
    
    def level_up(self):
        self.level += 1
        self.attack += 5
        self.defense += 2
        self.health = 100

class Enemy:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack
    
    def take_damage(self, damage):
        self.health -= damage

    
    def attack_enemy(self, player):
        damage = self.attack + random.randint(1, 3)
        player.take_damage(damage)

def display_status(player, enemy):
    print(f"{player.name} (Level {player.level}) - HP: {player.health}")
    print(f"{enemy.name} - HP: {enemy.health}")

def generate_random_description():
    descriptions = [
        "The battle is intense, sparks flying and swords clashing!",
        "You launch a powerful attack at the enemy!",
        "The enemy strikes with a swift and fierce blow!",
        "You dodge the enemy's attack with a nimble move!",
        "Blood stains the ground as the battle rages on!",
        "You muster all your strength for a final, decisive strike!"
    ]
    return random.choice(descriptions)

# 游戏主循环
def game_loop():
    player = Player()
    enemy = Enemy("Monster", 50, 8)
    
    while True:
        display_status(player, enemy)
        print("\nChoose your action:")
        print("1. Attack")
        print("2. Defend")
        # print("3. Exit")
        
        choice = input("Enter your choice 1 / 2: ")
        
        if choice == "1":
            print(generate_random_description())
            player.attack_enemy(enemy)
        elif choice == "2":
            print("You defended against the enemy's attack.")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Try again.")
            
        if enemy.health > 0:
            print("The enemy strikes back!")
            enemy.attack_enemy(player)
        elif enemy.health <= 0:
            print(f"You defeated the {enemy.name}!")
            player.level_up()
            enemy = Enemy("Monster", 100, 8)

# 运行游戏
game_loop()
