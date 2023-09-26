import random

upgrade_options = {}
available_options = ["最大生命值", "攻击力", "防御力", "恢复生命值", "速度", "暴击率", "命中率"]  # 可能有十几种选项

selected_options = random.sample(available_options, k=3)  # 从可选选项中随机选择 3 个选项

for i, option in enumerate(selected_options):
    key = str(i + 3)
    value = random.randint(1, 10)

    upgrade_options[key] = {"attribute": option, "value": value}

    print(f"{key}. {option} +{value}")

user_choice = input("请输入您的选择（输入对应的数字）：")

if user_choice in upgrade_options:
    option = upgrade_options[user_choice]
    attribute = option["attribute"]
    value = option["value"]
    print(f"您选择的是：{attribute} +{value}")
    # 根据用户选择更新属性值
    if attribute == "最大生命值":
        self.health_max += value
        self.health += value
    elif attribute == "攻击力":
        self.attack_max += value
        self.attack += value
    elif attribute == "防御力":
        self.defense_max += value
        self.defense += value
    elif attribute == "恢复生命值":
        self.health += value
        if self.health > self.health_max:
            self.health = self.health_max
    elif attribute == "速度":
        self.speed += value
    elif attribute == "暴击率":
        self.critical_rate += value
    elif attribute == "命中率":
        self.hit_rate += value

    print(f"你的{attribute}提升了{value}点！")
else:
    print("无效的选择！请重新选择。")
