# 웹 브라우저 없이 터미널에서 직접 실행할 수 있도록 수정한 Python 코드입니다.
# 사용법: 터미널에서 'python app.py' 명령어를 입력하세요.

import random
import json
import time

# --- 기존 게임 로직 (Player, CentoGameSimulator 클래스) ---
# (웹사이트의 코드와 동일한 로직이므로 간결성을 위해 생략합니다.
#  실제 파일에는 전체 코드가 포함되어 있습니다.)

class Player:
    def __init__(self, name): self.name = name; self.hand = []
    def add_card(self, card): self.hand.append(card); self.hand.sort()
    def remove_random_card(self):
        if not self.hand: return None
        card = random.choice(self.hand); self.hand.remove(card); return card
    def play_card_strategically(self, target_card):
        if not self.hand: return None
        best_card = min(self.hand, key=lambda card: abs(card - target_card))
        self.hand.remove(best_card); return best_card
    def discard_cards_in_range(self, low, high):
        to_discard = [c for c in self.hand if low < c < high]
        if to_discard: self.hand = [c for c in self.hand if c not in to_discard]
        return to_discard

class CentoGameSimulator:
    def __init__(self, player_names, cards_per_player=10):
        self.players=[Player(name) for name in player_names]; self.deck=list(range(1,101)); self.cards_per_player=cards_per_player; self.current_player_index=0; self.turn_number=1; self.game_over=False
    
    def get_game_state(self):
        return {
            "players": [{ "name": p.name, "cards": len(p.hand) } for p in self.players],
            "current_player_name": self.players[self.current_player_index].name if not self.game_over else None,
            "is_over": self.game_over,
            "turn_number": self.turn_number
        }

    def shuffle_and_deal(self):
        random.shuffle(self.deck)
        for _ in range(self.cards_per_player):
            for p in self.players:
                if self.deck: p.add_card(self.deck.pop())
        
        log = {
            "header": "게임 시작: 카드를 섞고 분배합니다.",
            "log_lines": [{ "type": "INIT_STATUS", "content": f"{p.name}: {p.hand}"} for p in self.players]
        }
        return { "log": log, "state": self.get_game_state() }

    def play_turn(self):
        if self.game_over: return { "log": None, "state": self.get_game_state() }
        
        cp = self.players[self.current_player_index]
        log_lines = [{"type": "INFO_HAND", "content": f"현재 손패: {cp.hand}"}]
        
        targets = [p for p in self.players if p != cp and p.hand]
        if not targets:
            self.game_over = True
            log_lines.append({"type": "INFO_MSG", "content": "카드를 뽑을 상대가 없어 게임을 종료합니다."})
        else:
            tp = random.choice(targets)
            drawn_card = tp.remove_random_card()
            log_lines.append({"type": "ACTION_DRAW", "content": f"{cp.name}이(가) {tp.name}에게서 카드를 뽑았습니다: [{drawn_card}]"})
            
            played_card = cp.play_card_strategically(drawn_card)
            if played_card is None:
                self.game_over = True
                log_lines.append({"type": "WIN", "content": f"{cp.name}이(가) 손에 카드가 없어 승리했습니다!"})
            else:
                log_lines.append({"type": "ACTION_PLAY", "content": f"{cp.name}이(가) 자신의 손에서 카드를 냈습니다: [{played_card}]"})
                low, high = min(drawn_card, played_card), max(drawn_card, played_card)
                
                if high - low <= 1:
                    log_lines.append({"type": "INFO_RANGE", "content": f"범위가 없습니다! ({low}~{high})"})
                else:
                    log_lines.append({"type": "INFO_RANGE", "content": f"생성된 범위: {low}~{high} (버릴 수 있는 카드: {low+1}~{high-1})"})
                    for p in self.players:
                        if p != cp:
                            discarded = p.discard_cards_in_range(low, high)
                            if discarded:
                                log_lines.append({"type": "ACTION_DISCARD", "content": f"{p.name}이(가) 카드를 버렸습니다: {discarded}"})
                            if not p.hand: self.game_over = True; log_lines.append({"type": "WIN", "content": f"{p.name}이(가) 모든 카드를 버려 승리했습니다!"}); break
                
                if not cp.hand and not self.game_over:
                    self.game_over = True
                    log_lines.append({"type": "WIN", "content": f"{cp.name}이(가) 마지막 카드를 내어 승리했습니다!"})
        
        turn_header_text = f"턴 {self.turn_number}: {cp.name}의 차례"
        if self.game_over:
            winner = next((p for p in self.players if not p.hand), None)
            if winner: 
                log_lines.append({"type": "WINNER", "content": f"🎉 최종 승자는 {winner.name}입니다! 🎉"})
                turn_header_text = f"게임 종료: {winner.name} 승리!"
            else: 
                log_lines.append({"type": "INFO_MSG", "content": "승자 없이 게임이 종료되었습니다."})
                turn_header_text = "게임 종료"
        
        if not self.game_over:
             self.current_player_index = (self.current_player_index + 1) % len(self.players)
             self.turn_number += 1

        log = { "header": turn_header_text, "log_lines": log_lines }
        return { "log": log, "state": self.get_game_state() }


# --- 터미널 실행을 위한 추가 코드 ---

def print_log(log_data):
    """터미널에 로그를 예쁘게 출력하는 함수"""
    if not log_data:
        return

    print("\n" + "="*50)
    print(f"| {log_data['header']:^46} |")
    print("="*50)

    for line in log_data['log_lines']:
        print(f"  - {line['content']}")
    
    print("="*50)

def print_player_status(state_data):
    """터미널에 플레이어 상태를 출력하는 함수"""
    print("\n--- 플레이어 현황 ---")
    for player in state_data['players']:
        status = "현재 턴" if player['name'] == state_data['current_player_name'] else ""
        print(f"  - {player['name']}: 남은 카드 {player['cards']}장 {status}")
    print("-" * 23 + "\n")


if __name__ == "__main__":
    # 게임 인스턴스 생성
    player_list = ["플레이어1", "플레이어2", "플레이어3", "플레이어4"]
    game = CentoGameSimulator(player_list, 10)

    # 게임 시작 및 초기 상태 출력
    initial_data = game.shuffle_and_deal()
    print_log(initial_data['log'])
    print_player_status(initial_data['state'])

    # 게임 루프: 게임이 끝날 때까지 턴을 진행
    while not game.game_over:
        input("엔터 키를 눌러 다음 턴을 진행하세요...")
        turn_data = game.play_turn()
        print_log(turn_data['log'])
        print_player_status(turn_data['state'])
    
    print("\n >> 게임이 종료되었습니다. << \n")
