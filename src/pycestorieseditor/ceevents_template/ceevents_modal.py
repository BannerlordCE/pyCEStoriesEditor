from attrs import define, field
from enum import Enum
from typing import List, Optional


@define
class AgreeResultText:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class AgreeText:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class Background:
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
        }
    )
    weight: Optional[str] = field(
        default=None,
        metadata={
            "name": "Weight",
            "type": "Attribute",
        }
    )
    use_conditions: Optional[str] = field(
        default=None,
        metadata={
            "name": "UseConditions",
            "type": "Attribute",
        }
    )


@define
class BackgroundAnimationSpeed:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        }
    )


@define
class BackgroundName:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class BackgroundNames:
    background_name: List[str] = field(
        factory=list,
        metadata={
            "name": "BackgroundName",
            "type": "Element",
            "namespace": "",
        }
    )


@define
class CanOnlyHappenNrOfTimes:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class CancelText:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class CaptorGoldTotal:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ClanOption:
    ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "Ref",
            "type": "Attribute",
        }
    )
    action: Optional[str] = field(
        default=None,
        metadata={
            "name": "Action",
            "type": "Attribute",
        }
    )
    clan: Optional[str] = field(
        default=None,
        metadata={
            "name": "Clan",
            "type": "Attribute",
        }
    )
    hide_notification: Optional[bool] = field(
        default=None,
        metadata={
            "name": "HideNotification",
            "type": "Attribute",
        }
    )


@define
class CustomFlags:
    custom_flag: List[str] = field(
        factory=list,
        metadata={
            "name": "CustomFlag",
            "type": "Element",
            "namespace": "",
        }
    )


@define
class DamageParty:
    number: Optional[str] = field(
        default=None,
        metadata={
            "name": "Number",
            "type": "Attribute",
        }
    )
    wounded_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "WoundedNumber",
            "type": "Attribute",
        }
    )
    include_heroes: Optional[str] = field(
        default=None,
        metadata={
            "name": "IncludeHeroes",
            "type": "Attribute",
        }
    )
    ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "Ref",
            "type": "Attribute",
        }
    )


@define
class EscapeChance:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class Flag:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class GoldTotal:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class HealthTotal:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class IsCancelOptional:
    value: Optional[bool] = field(
        default=None,
        metadata={
            "required": True,
        }
    )


@define
class ItemToGive:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class KingdomOption:
    ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "Ref",
            "type": "Attribute",
        }
    )
    action: Optional[str] = field(
        default=None,
        metadata={
            "name": "Action",
            "type": "Attribute",
        }
    )
    kingdom: Optional[str] = field(
        default=None,
        metadata={
            "name": "Kingdom",
            "type": "Attribute",
        }
    )
    hide_notification: Optional[bool] = field(
        default=None,
        metadata={
            "name": "HideNotification",
            "type": "Attribute",
        }
    )


@define
class MoraleTotal:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class Name:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class NotificationName:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class OrderToCall:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class PregnancyRiskModifier:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ProstitutionTotal:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class RelationTotal:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class RenownTotal:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqCaptivesAbove:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqCaptivesBelow:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqCaptorPartyHaveItem:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqCaptorSkill:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqCaptorSkillLevelAbove:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqCaptorSkillLevelBelow:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqCaptorTrait:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqCaptorTraitLevelAbove:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqCaptorTraitLevelBelow:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqCustomCode:
    value: Optional[bool] = field(
        default=None,
        metadata={
            "required": True,
        }
    )


@define
class ReqFemaleCaptivesAbove:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqFemaleCaptivesBelow:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqFemaleTroopsAbove:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqFemaleTroopsBelow:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqGoldAbove:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqGoldBelow:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqHeroCaptivesAbove:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqHeroCaptivesBelow:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqHeroCaptorRelationAbove:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqHeroCaptorRelationBelow:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqHeroFemaleCaptivesAbove:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqHeroFemaleCaptivesBelow:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqHeroFemaleTroopsAbove:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqHeroFemaleTroopsBelow:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqHeroHealthAbovePercentage:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqHeroHealthBelowPercentage:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqHeroMaleCaptivesAbove:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqHeroMaleCaptivesBelow:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqHeroMaleTroopsAbove:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqHeroMaleTroopsBelow:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqHeroMaxAge:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqHeroMinAge:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqHeroPartyHaveItem:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqHeroProstituteLevelAbove:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqHeroProstituteLevelBelow:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqHeroSkill:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqHeroSkillLevelAbove:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqHeroSkillLevelBelow:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqHeroSlaveLevelAbove:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqHeroSlaveLevelBelow:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqHeroTrait:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqHeroTraitLevelAbove:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqHeroTraitLevelBelow:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqHeroTroopsAbove:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqHeroTroopsBelow:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqMaleCaptivesAbove:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqMaleCaptivesBelow:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqMaleTroopsAbove:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqMaleTroopsBelow:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqMoraleAbove:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqMoraleBelow:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqTroopsAbove:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class ReqTroopsBelow:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


class RestrictedListOfConsequencesValue(Enum):
    GIVE_ITEM = "GiveItem"
    GIVE_XP = "GiveXP"
    GIVE_GOLD = "GiveGold"
    GIVE_CAPTOR_GOLD = "GiveCaptorGold"
    CHANGE_PROSTITUTION_LEVEL = "ChangeProstitutionLevel"
    CHANGE_SLAVERY_LEVEL = "ChangeSlaveryLevel"
    ADD_PROSTITUTION_FLAG = "AddProstitutionFlag"
    REMOVE_PROSTITUTION_FLAG = "RemoveProstitutionFlag"
    ADD_SLAVERY_FLAG = "AddSlaveryFlag"
    REMOVE_SLAVERY_FLAG = "RemoveSlaveryFlag"
    CHANGE_MORALE = "ChangeMorale"
    CHANGE_RENOWN = "ChangeRenown"
    CHANGE_CAPTOR_RENOWN = "ChangeCaptorRenown"
    CHANGE_HEALTH = "ChangeHealth"
    CHANGE_RELATION = "ChangeRelation"
    CHANGE_TRAIT = "ChangeTrait"
    CHANGE_CAPTOR_TRAIT = "ChangeCaptorTrait"
    CHANGE_SKILL = "ChangeSkill"
    CHANGE_CAPTOR_SKILL = "ChangeCaptorSkill"
    IMPREGNATION_RISK = "ImpregnationRisk"
    IMPREGNATION_HERO = "ImpregnationHero"
    IMPREGNATION_BY_PLAYER = "ImpregnationByPlayer"
    CAPTOR_LEAVE_SPOUSE = "CaptorLeaveSpouse"
    CAPTIVE_LEAVE_SPOUSE = "CaptiveLeaveSpouse"
    CAPTIVE_MARRY_CAPTOR = "CaptiveMarryCaptor"
    CHANGE_GOLD = "ChangeGold"
    CHANGE_CAPTOR_GOLD = "ChangeCaptorGold"
    ATTEMPT_ESCAPE = "AttemptEscape"
    ESCAPE = "Escape"
    ESCAPE_ICON = "EscapeIcon"
    LEAVE = "Leave"
    CONTINUE = "Continue"
    EMPTY_ICON = "EmptyIcon"
    WAIT = "Wait"
    BRIBE_AND_ESCAPE = "BribeAndEscape"
    SUBMENU = "Submenu"
    RANSOM_AND_BRIBE = "RansomAndBribe"
    TRADE = "Trade"
    GIVE_BIRTH = "GiveBirth"
    ABORT = "Abort"
    SOLD_TO_CARAVAN = "SoldToCaravan"
    SOLD_TO_SETTLEMENT = "SoldToSettlement"
    SOLD_TO_LORD_PARTY = "SoldToLordParty"
    SOLD_TO_NOTABLE = "SoldToNotable"
    TELEPORT_PLAYER = "TeleportPlayer"
    CAPTURE_PLAYER = "CapturePlayer"
    GAIN_RANDOM_PRISONERS = "GainRandomPrisoners"
    REBEL_PRISONERS = "RebelPrisoners"
    HUNT_PRISONERS = "HuntPrisoners"
    START_BATTLE = "StartBattle"
    RELEASE_RANDOM_PRISONERS = "ReleaseRandomPrisoners"
    RELEASE_ALL_PRISONERS = "ReleaseAllPrisoners"
    KILL_RANDOM_PRISONERS = "KillRandomPrisoners"
    KILL_ALL_PRISONERS = "KillAllPrisoners"
    KILL_PRISONER = "KillPrisoner"
    KILL_CAPTOR = "KillCaptor"
    KILL_RANDOM_TROOPS = "KillRandomTroops"
    WOUND_RANDOM_PRISONERS = "WoundRandomPrisoners"
    WOUND_ALL_PRISONERS = "WoundAllPrisoners"
    WOUND_PRISONER = "WoundPrisoner"
    WOUND_CAPTOR = "WoundCaptor"
    WOUND_RANDOM_TROOPS = "WoundRandomTroops"
    JOIN_CAPTOR = "JoinCaptor"
    MAKE_HERO_COMPANION = "MakeHeroCompanion"
    STRIP = "Strip"
    STRIP_HERO = "StripHero"
    STRIP_PLAYER = "StripPlayer"
    PLAYER_IS_NOT_BUSY = "PlayerIsNotBusy"
    PLAYER_ALLOWED_COMPANION = "PlayerAllowedCompanion"
    INFORMATION_MESSAGE = "InformationMessage"
    NO_MESSAGES = "NoMessages"


class RestrictedListOfFlagsType(Enum):
    CAN_ONLY_BE_TRIGGERED_BY_OTHER_EVENT = "CanOnlyBeTriggeredByOtherEvent"
    RANDOM = "Random"
    CAPTOR = "Captor"
    CAPTIVE = "Captive"
    OVERWRITEABLE = "Overwriteable"
    COMMON = "Common"
    FEMDOM = "Femdom"
    BESTIALITY = "Bestiality"
    PROSTITUTION = "Prostitution"
    ROMANCE = "Romance"
    SLAVERY = "Slavery"
    STRAIGHT = "Straight"
    LESBIAN = "Lesbian"
    GAY = "Gay"
    CARAVAN_PARTY = "CaravanParty"
    BANDIT_PARTY = "BanditParty"
    LORD_PARTY = "LordParty"
    DEFAULT_PARTY = "DefaultParty"
    NOTABLE_FEMALES_NEARBY = "NotableFemalesNearby"
    NOTABLE_MALES_NEARBY = "NotableMalesNearby"
    VISITED_BY_CARAVAN = "VisitedByCaravan"
    VISITED_BY_LORD = "VisitedByLord"
    DURING_SIEGE = "DuringSiege"
    DURING_RAID = "DuringRaid"
    LOCATION_TRAVELLING_PARTY = "LocationTravellingParty"
    LOCATION_PARTY_IN_TOWN = "LocationPartyInTown"
    LOCATION_PARTY_IN_CASTLE = "LocationPartyInCastle"
    LOCATION_PARTY_IN_VILLAGE = "LocationPartyInVillage"
    LOCATION_DUNGEON = "LocationDungeon"
    LOCATION_VILLAGE = "LocationVillage"
    LOCATION_CITY = "LocationCity"
    LOCATION_CASTLE = "LocationCastle"
    LOCATION_HIDEOUT = "LocationHideout"
    LOCATION_TAVERN = "LocationTavern"
    PLAYER_IS_NOT_BUSY = "PlayerIsNotBusy"
    PLAYER_ALLOWED_COMPANION = "PlayerAllowedCompanion"
    STRIP_ENABLED = "StripEnabled"
    STRIP_DISABLED = "StripDisabled"
    CAPTIVES_OUT_NUMBER = "CaptivesOutNumber"
    TIME_NIGHT = "TimeNight"
    TIME_DAY = "TimeDay"
    SEASON_WINTER = "SeasonWinter"
    SEASON_SPRING = "SeasonSpring"
    SEASON_SUMMER = "SeasonSummer"
    SEASON_FALL = "SeasonFall"
    OWNER_GENDER_IS_FEMALE = "OwnerGenderIsFemale"
    OWNER_GENDER_IS_MALE = "OwnerGenderIsMale"
    CAPTOR_IS_HERO = "CaptorIsHero"
    CAPTOR_IS_NON_HERO = "CaptorIsNonHero"
    CAPTOR_GENDER_IS_FEMALE = "CaptorGenderIsFemale"
    CAPTOR_GENDER_IS_MALE = "CaptorGenderIsMale"
    CAPTOR_HAVE_OFFSPRING = "CaptorHaveOffspring"
    CAPTOR_NOT_HAVE_OFFSPRING = "CaptorNotHaveOffspring"
    CAPTOR_HAVE_SPOUSE = "CaptorHaveSpouse"
    CAPTOR_NOT_HAVE_SPOUSE = "CaptorNotHaveSpouse"
    CAPTOR_OWNS_CURRENT_SETTLEMENT = "CaptorOwnsCurrentSettlement"
    CAPTOR_OWNS_NOT_CURRENT_SETTLEMENT = "CaptorOwnsNotCurrentSettlement"
    CAPTOR_FACTION_OWNS_SETTLEMENT = "CaptorFactionOwnsSettlement"
    CAPTOR_NEUTRAL_FACTION_OWNS_SETTLEMENT = "CaptorNeutralFactionOwnsSettlement"
    CAPTOR_ENEMY_FACTION_OWNS_SETTLEMENT = "CaptorEnemyFactionOwnsSettlement"
    CAPTIVE_IS_HERO = "CaptiveIsHero"
    CAPTIVE_IS_NON_HERO = "CaptiveIsNonHero"
    HERO_GENDER_IS_FEMALE = "HeroGenderIsFemale"
    HERO_GENDER_IS_MALE = "HeroGenderIsMale"
    HERO_HAVE_OFFSPRING = "HeroHaveOffspring"
    HERO_NOT_HAVE_OFFSPRING = "HeroNotHaveOffspring"
    HERO_HAVE_SPOUSE = "HeroHaveSpouse"
    HERO_NOT_HAVE_SPOUSE = "HeroNotHaveSpouse"
    HERO_IS_PREGNANT = "HeroIsPregnant"
    HERO_IS_NOT_PREGNANT = "HeroIsNotPregnant"
    HERO_OWNS_FIEF = "HeroOwnsFief"
    HERO_OWNS_NO_FIEF = "HeroOwnsNoFief"
    HERO_IS_CLAN_LEADER = "HeroIsClanLeader"
    HERO_IS_NOT_CLAN_LEADER = "HeroIsNotClanLeader"
    HERO_IS_FACTION_LEADER = "HeroIsFactionLeader"
    HERO_IS_NOT_FACTION_LEADER = "HeroIsNotFactionLeader"
    HERO_OWNS_CURRENT_PARTY = "HeroOwnsCurrentParty"
    HERO_OWNS_NOT_CURRENT_PARTY = "HeroOwnsNotCurrentParty"
    HERO_FACTION_OWNS_PARTY = "HeroFactionOwnsParty"
    HERO_NEUTRAL_FACTION_OWNS_PARTY = "HeroNeutralFactionOwnsParty"
    HERO_ENEMY_FACTION_OWNS_PARTY = "HeroEnemyFactionOwnsParty"
    HERO_OWNS_CURRENT_SETTLEMENT = "HeroOwnsCurrentSettlement"
    HERO_OWNS_NOT_CURRENT_SETTLEMENT = "HeroOwnsNotCurrentSettlement"
    HERO_FACTION_OWNS_SETTLEMENT = "HeroFactionOwnsSettlement"
    HERO_NEUTRAL_FACTION_OWNS_SETTLEMENT = "HeroNeutralFactionOwnsSettlement"
    HERO_ENEMY_FACTION_OWNS_SETTLEMENT = "HeroEnemyFactionOwnsSettlement"
    HERO_OWNED_BY_NOTABLE = "HeroOwnedByNotable"
    HERO_NOT_OWNED_BY_NOTABLE = "HeroNotOwnedByNotable"
    HERO_IS_PROSTITUTE = "HeroIsProstitute"
    HERO_IS_NOT_PROSTITUTE = "HeroIsNotProstitute"
    HERO_IS_SLAVE = "HeroIsSlave"
    HERO_IS_NOT_SLAVE = "HeroIsNotSlave"
    PLAYER_OWNS_BROTHEL_IN_SETTLEMENT = "PlayerOwnsBrothelInSettlement"
    PLAYER_OWNS_NOT_BROTHEL_IN_SETTLEMENT = "PlayerOwnsNotBrothelInSettlement"
    IGNORE_ALL_OTHER = "IgnoreAllOther"
    DEATH_ALTERNATIVE = "DeathAlternative"
    DESERTION_ALTERNATIVE = "DesertionAlternative"
    MARRIAGE_ALTERNATIVE = "MarriageAlternative"
    BIRTH_ALTERNATIVE = "BirthAlternative"
    WAITING_MENU = "WaitingMenu"
    PROGRESS_MENU = "ProgressMenu"


@define
class SceneSettings:
    talk_to: Optional[str] = field(
        default=None,
        metadata={
            "name": "TalkTo",
            "type": "Attribute",
        }
    )
    scene_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "SceneName",
            "type": "Attribute",
        }
    )


@define
class SceneToPlay:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class SexualContent:
    value: Optional[bool] = field(
        default=None,
        metadata={
            "required": True,
        }
    )


@define
class Skill:
    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    by_level: Optional[str] = field(
        default=None,
        metadata={
            "name": "ByLevel",
            "type": "Attribute",
        }
    )
    by_xp: Optional[str] = field(
        default=None,
        metadata={
            "name": "ByXP",
            "type": "Attribute",
        }
    )
    ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "Ref",
            "type": "Attribute",
        }
    )
    color: Optional[str] = field(
        default=None,
        metadata={
            "name": "Color",
            "type": "Attribute",
        }
    )
    hide_notification: Optional[bool] = field(
        default=None,
        metadata={
            "name": "HideNotification",
            "type": "Attribute",
        }
    )


@define
class SkillRequired:
    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    max: Optional[str] = field(
        default=None,
        metadata={
            "name": "Max",
            "type": "Attribute",
        }
    )
    min: Optional[str] = field(
        default=None,
        metadata={
            "name": "Min",
            "type": "Attribute",
        }
    )
    ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "Ref",
            "type": "Attribute",
        }
    )


@define
class SkillToLevel:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class SkillTotal:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class SkillXptotal:
    class Meta:
        name = "SkillXPTotal"

    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class SlaveryTotal:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class SoundName:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class SpawnTroop:
    ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "Ref",
            "type": "Attribute",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    number: Optional[str] = field(
        default=None,
        metadata={
            "name": "Number",
            "type": "Attribute",
        }
    )
    wounded_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "WoundedNumber",
            "type": "Attribute",
        }
    )


@define
class StringContent:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class StripSettings:
    custom_body: List[str] = field(
        factory=list,
        metadata={
            "name": "CustomBody",
            "type": "Element",
            "namespace": "",
            "sequential": True,
        }
    )
    custom_cape: List[str] = field(
        factory=list,
        metadata={
            "name": "CustomCape",
            "type": "Element",
            "namespace": "",
            "sequential": True,
        }
    )
    custom_gloves: List[str] = field(
        factory=list,
        metadata={
            "name": "CustomGloves",
            "type": "Element",
            "namespace": "",
            "sequential": True,
        }
    )
    custom_legs: List[str] = field(
        factory=list,
        metadata={
            "name": "CustomLegs",
            "type": "Element",
            "namespace": "",
            "sequential": True,
        }
    )
    custom_head: List[str] = field(
        factory=list,
        metadata={
            "name": "CustomHead",
            "type": "Element",
            "namespace": "",
            "sequential": True,
        }
    )
    clothing: List[str] = field(
        factory=list,
        metadata={
            "name": "Clothing",
            "type": "Element",
            "namespace": "",
            "sequential": True,
        }
    )
    mount: List[str] = field(
        factory=list,
        metadata={
            "name": "Mount",
            "type": "Element",
            "namespace": "",
            "sequential": True,
        }
    )
    melee: List[str] = field(
        factory=list,
        metadata={
            "name": "Melee",
            "type": "Element",
            "namespace": "",
            "sequential": True,
        }
    )
    ranged: List[str] = field(
        factory=list,
        metadata={
            "name": "Ranged",
            "type": "Element",
            "namespace": "",
            "sequential": True,
        }
    )
    forced: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Forced",
            "type": "Attribute",
        }
    )
    quest_enabled: Optional[bool] = field(
        default=None,
        metadata={
            "name": "QuestEnabled",
            "type": "Attribute",
        }
    )


@define
class TeleportSettings:
    location: Optional[str] = field(
        default=None,
        metadata={
            "name": "Location",
            "type": "Attribute",
        }
    )
    location_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "LocationName",
            "type": "Attribute",
        }
    )
    distance: Optional[str] = field(
        default=None,
        metadata={
            "name": "Distance",
            "type": "Attribute",
        }
    )
    faction: Optional[str] = field(
        default=None,
        metadata={
            "name": "Faction",
            "type": "Attribute",
        }
    )


class TerrainTypeValue(Enum):
    WATER = "Water"
    MOUNTAIN = "Mountain"
    SNOW = "Snow"
    STEPPE = "Steppe"
    PLAIN = "Plain"
    DESERT = "Desert"
    SWAMP = "Swamp"
    DUNE = "Dune"
    BRIDGE = "Bridge"
    RIVER = "River"
    FOREST = "Forest"
    SHALLOW_RIVER = "ShallowRiver"
    LAKE = "Lake"
    CANYON = "Canyon"
    RURAL_AREA = "RuralArea"


@define
class Text:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class Trait:
    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    by_level: Optional[str] = field(
        default=None,
        metadata={
            "name": "ByLevel",
            "type": "Attribute",
        }
    )
    by_xp: Optional[str] = field(
        default=None,
        metadata={
            "name": "ByXP",
            "type": "Attribute",
        }
    )
    ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "Ref",
            "type": "Attribute",
        }
    )
    color: Optional[str] = field(
        default=None,
        metadata={
            "name": "Color",
            "type": "Attribute",
        }
    )
    hide_notification: Optional[bool] = field(
        default=None,
        metadata={
            "name": "HideNotification",
            "type": "Attribute",
        }
    )


@define
class TraitRequired:
    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    max: Optional[str] = field(
        default=None,
        metadata={
            "name": "Max",
            "type": "Attribute",
        }
    )
    min: Optional[str] = field(
        default=None,
        metadata={
            "name": "Min",
            "type": "Attribute",
        }
    )
    ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "Ref",
            "type": "Attribute",
        }
    )


@define
class TraitToLevel:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class TraitTotal:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class TraitXptotal:
    class Meta:
        name = "TraitXPTotal"

    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class TriggerEvent:
    event_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "EventName",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    event_weight: Optional[str] = field(
        default=None,
        metadata={
            "name": "EventWeight",
            "type": "Element",
            "namespace": "",
        }
    )
    event_use_conditions: Optional[str] = field(
        default=None,
        metadata={
            "name": "EventUseConditions",
            "type": "Element",
            "namespace": "",
        }
    )


@define
class WeightedChanceOfOccuring:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@define
class BackgroundAnimation(BackgroundNames):
    pass


@define
class Backgrounds:
    background: List[Background] = field(
        factory=list,
        metadata={
            "name": "Background",
            "type": "Element",
            "min_occurs": 1,
        }
    )


@define
class ClanOptions:
    clan_option: List[ClanOption] = field(
        factory=list,
        metadata={
            "name": "ClanOption",
            "type": "Element",
            "min_occurs": 1,
        }
    )


@define
class KingdomOptions:
    kingdom_option: List[KingdomOption] = field(
        factory=list,
        metadata={
            "name": "KingdomOption",
            "type": "Element",
            "min_occurs": 1,
        }
    )


@define
class MultipleListOfCustomFlags(CustomFlags):
    pass


@define
class MultipleRestrictedListOfConsequences:
    restricted_list_of_consequences: List[RestrictedListOfConsequencesValue] = field(
        factory=list,
        metadata={
            "name": "RestrictedListOfConsequences",
            "type": "Element",
            "min_occurs": 1,
        }
    )


@define
class MultipleRestrictedListOfFlags:
    restricted_list_of_flags: List[RestrictedListOfFlagsType] = field(
        factory=list,
        metadata={
            "name": "RestrictedListOfFlags",
            "type": "Element",
        }
    )


@define
class RestrictedListOfConsequences:
    value: Optional[RestrictedListOfConsequencesValue] = field(
        default=None
    )


@define
class RestrictedListOfFlags:
    value: Optional[RestrictedListOfFlagsType] = field(
        default=None,
        metadata={
            "required": True,
        }
    )


@define
class SkillsRequired:
    skill_required: List[SkillRequired] = field(
        factory=list,
        metadata={
            "name": "SkillRequired",
            "type": "Element",
            "min_occurs": 1,
        }
    )


@define
class SkillsToLevel:
    skill: List[Skill] = field(
        factory=list,
        metadata={
            "name": "Skill",
            "type": "Element",
            "min_occurs": 1,
        }
    )


@define
class SpawnTroops:
    spawn_troop: List[SpawnTroop] = field(
        factory=list,
        metadata={
            "name": "SpawnTroop",
            "type": "Element",
            "min_occurs": 1,
        }
    )


@define
class TerrainType:
    value: Optional[TerrainTypeValue] = field(
        default=None
    )


@define
class TerrainTypes:
    terrain_type: List[TerrainTypeValue] = field(
        factory=list,
        metadata={
            "name": "TerrainType",
            "type": "Element",
            "min_occurs": 1,
        }
    )


@define
class TraitsRequired:
    trait_required: List[TraitRequired] = field(
        factory=list,
        metadata={
            "name": "TraitRequired",
            "type": "Element",
            "min_occurs": 1,
        }
    )


@define
class TraitsToLevel:
    trait: List[Trait] = field(
        factory=list,
        metadata={
            "name": "Trait",
            "type": "Element",
            "min_occurs": 1,
        }
    )


@define
class TriggerEvents:
    trigger_event: List[TriggerEvent] = field(
        factory=list,
        metadata={
            "name": "TriggerEvent",
            "type": "Element",
            "min_occurs": 1,
        }
    )


@define
class BattleSettings:
    spawn_troops: Optional[SpawnTroops] = field(
        default=None,
        metadata={
            "name": "SpawnTroops",
            "type": "Element",
        }
    )
    ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "Ref",
            "type": "Attribute",
        }
    )
    victory: Optional[str] = field(
        default=None,
        metadata={
            "name": "Victory",
            "type": "Attribute",
        }
    )
    defeat: Optional[str] = field(
        default=None,
        metadata={
            "name": "Defeat",
            "type": "Attribute",
        }
    )
    enemy_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "EnemyName",
            "type": "Attribute",
        }
    )
    player_troops: Optional[str] = field(
        default=None,
        metadata={
            "name": "PlayerTroops",
            "type": "Attribute",
        }
    )


@define
class Companion:
    multiple_restricted_list_of_consequences: Optional[MultipleRestrictedListOfConsequences] = field(
        default=None,
        metadata={
            "name": "MultipleRestrictedListOfConsequences",
            "type": "Element",
        }
    )
    pregnancy_risk_modifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "PregnancyRiskModifier",
            "type": "Element",
        }
    )
    escape_chance: Optional[str] = field(
        default=None,
        metadata={
            "name": "EscapeChance",
            "type": "Element",
        }
    )
    gold_total: Optional[str] = field(
        default=None,
        metadata={
            "name": "GoldTotal",
            "type": "Element",
        }
    )
    captor_gold_total: Optional[str] = field(
        default=None,
        metadata={
            "name": "CaptorGoldTotal",
            "type": "Element",
        }
    )
    relation_total: Optional[str] = field(
        default=None,
        metadata={
            "name": "RelationTotal",
            "type": "Element",
        }
    )
    morale_total: Optional[str] = field(
        default=None,
        metadata={
            "name": "MoraleTotal",
            "type": "Element",
        }
    )
    health_total: Optional[str] = field(
        default=None,
        metadata={
            "name": "HealthTotal",
            "type": "Element",
        }
    )
    renown_total: Optional[str] = field(
        default=None,
        metadata={
            "name": "RenownTotal",
            "type": "Element",
        }
    )
    skills_to_level: Optional[SkillsToLevel] = field(
        default=None,
        metadata={
            "name": "SkillsToLevel",
            "type": "Element",
        }
    )
    traits_to_level: Optional[TraitsToLevel] = field(
        default=None,
        metadata={
            "name": "TraitsToLevel",
            "type": "Element",
        }
    )
    kingdom_options: Optional[KingdomOptions] = field(
        default=None,
        metadata={
            "name": "KingdomOptions",
            "type": "Element",
        }
    )
    clan_options: Optional[ClanOptions] = field(
        default=None,
        metadata={
            "name": "ClanOptions",
            "type": "Element",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "Ref",
            "type": "Attribute",
        }
    )
    type: Optional[str] = field(
        default=None,
        metadata={
            "name": "Type",
            "type": "Attribute",
        }
    )
    location: Optional[str] = field(
        default=None,
        metadata={
            "name": "Location",
            "type": "Attribute",
        }
    )
    use_other_conditions: Optional[str] = field(
        default=None,
        metadata={
            "name": "UseOtherConditions",
            "type": "Attribute",
        }
    )


@define
class DelayEvent:
    use_conditions: List[str] = field(
        factory=list,
        metadata={
            "name": "UseConditions",
            "type": "Element",
            "namespace": "",
            "sequential": True,
        }
    )
    time_to_take: List[str] = field(
        factory=list,
        metadata={
            "name": "TimeToTake",
            "type": "Element",
            "namespace": "",
            "sequential": True,
        }
    )
    trigger_event_name: List[str] = field(
        factory=list,
        metadata={
            "name": "TriggerEventName",
            "type": "Element",
            "namespace": "",
            "sequential": True,
        }
    )
    trigger_events: List[TriggerEvents] = field(
        factory=list,
        metadata={
            "name": "TriggerEvents",
            "type": "Element",
            "sequential": True,
        }
    )


@define
class ProgressEvent:
    should_stop_moving: List[bool] = field(
        factory=list,
        metadata={
            "name": "ShouldStopMoving",
            "type": "Element",
            "namespace": "",
            "sequential": True,
        }
    )
    display_progress_mode: List[str] = field(
        factory=list,
        metadata={
            "name": "DisplayProgressMode",
            "type": "Element",
            "namespace": "",
            "sequential": True,
        }
    )
    time_to_take: List[str] = field(
        factory=list,
        metadata={
            "name": "TimeToTake",
            "type": "Element",
            "namespace": "",
            "sequential": True,
        }
    )
    trigger_event_name: List[str] = field(
        factory=list,
        metadata={
            "name": "TriggerEventName",
            "type": "Element",
            "namespace": "",
            "sequential": True,
        }
    )
    trigger_events: List[TriggerEvents] = field(
        factory=list,
        metadata={
            "name": "TriggerEvents",
            "type": "Element",
            "sequential": True,
        }
    )


@define
class SpawnHero:
    skills_to_level: Optional[SkillsToLevel] = field(
        default=None,
        metadata={
            "name": "SkillsToLevel",
            "type": "Element",
        }
    )
    ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "Ref",
            "type": "Attribute",
        }
    )
    culture: Optional[str] = field(
        default=None,
        metadata={
            "name": "Culture",
            "type": "Attribute",
        }
    )
    gender: Optional[str] = field(
        default=None,
        metadata={
            "name": "Gender",
            "type": "Attribute",
        }
    )
    clan: Optional[str] = field(
        default=None,
        metadata={
            "name": "Clan",
            "type": "Attribute",
        }
    )


@define
class TerrainTypesRequirements:
    terrain_types: List[TerrainTypes] = field(
        factory=list,
        metadata={
            "name": "TerrainTypes",
            "type": "Element",
            "min_occurs": 1,
        }
    )


@define
class Companions:
    companion: List[Companion] = field(
        factory=list,
        metadata={
            "name": "Companion",
            "type": "Element",
            "min_occurs": 1,
        }
    )


@define
class SpawnHeroes:
    spawn_hero: List[SpawnHero] = field(
        factory=list,
        metadata={
            "name": "SpawnHero",
            "type": "Element",
            "min_occurs": 1,
        }
    )


@define
class Option:
    order: Optional[str] = field(
        default=None,
        metadata={
            "name": "Order",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    multiple_restricted_list_of_consequences: Optional[MultipleRestrictedListOfConsequences] = field(
        default=None,
        metadata={
            "name": "MultipleRestrictedListOfConsequences",
            "type": "Element",
            "required": True,
        }
    )
    option_text: Optional[str] = field(
        default=None,
        metadata={
            "name": "OptionText",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    trigger_event_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "TriggerEventName",
            "type": "Element",
            "namespace": "",
        }
    )
    sound_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "SoundName",
            "type": "Element",
        }
    )
    scene_to_play: Optional[str] = field(
        default=None,
        metadata={
            "name": "SceneToPlay",
            "type": "Element",
        }
    )
    pregnancy_risk_modifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "PregnancyRiskModifier",
            "type": "Element",
        }
    )
    escape_chance: Optional[str] = field(
        default=None,
        metadata={
            "name": "EscapeChance",
            "type": "Element",
        }
    )
    req_hero_party_have_item: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroPartyHaveItem",
            "type": "Element",
        }
    )
    req_captor_party_have_item: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqCaptorPartyHaveItem",
            "type": "Element",
        }
    )
    req_hero_health_below_percentage: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroHealthBelowPercentage",
            "type": "Element",
        }
    )
    req_hero_health_above_percentage: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroHealthAbovePercentage",
            "type": "Element",
        }
    )
    req_hero_captor_relation_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroCaptorRelationAbove",
            "type": "Element",
        }
    )
    req_hero_captor_relation_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroCaptorRelationBelow",
            "type": "Element",
        }
    )
    req_hero_prostitute_level_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroProstituteLevelAbove",
            "type": "Element",
        }
    )
    req_hero_prostitute_level_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroProstituteLevelBelow",
            "type": "Element",
        }
    )
    req_hero_slave_level_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroSlaveLevelAbove",
            "type": "Element",
        }
    )
    req_hero_slave_level_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroSlaveLevelBelow",
            "type": "Element",
        }
    )
    req_hero_trait_level_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroTraitLevelAbove",
            "type": "Element",
        }
    )
    req_hero_trait_level_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroTraitLevelBelow",
            "type": "Element",
        }
    )
    req_captor_trait_level_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqCaptorTraitLevelAbove",
            "type": "Element",
        }
    )
    req_captor_trait_level_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqCaptorTraitLevelBelow",
            "type": "Element",
        }
    )
    req_hero_skill_level_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroSkillLevelAbove",
            "type": "Element",
        }
    )
    req_hero_skill_level_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroSkillLevelBelow",
            "type": "Element",
        }
    )
    req_captor_skill_level_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqCaptorSkillLevelAbove",
            "type": "Element",
        }
    )
    req_captor_skill_level_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqCaptorSkillLevelBelow",
            "type": "Element",
        }
    )
    req_troops_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqTroopsAbove",
            "type": "Element",
        }
    )
    req_troops_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqTroopsBelow",
            "type": "Element",
        }
    )
    req_captives_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqCaptivesAbove",
            "type": "Element",
        }
    )
    req_captives_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqCaptivesBelow",
            "type": "Element",
        }
    )
    req_female_troops_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqFemaleTroopsAbove",
            "type": "Element",
        }
    )
    req_female_troops_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqFemaleTroopsBelow",
            "type": "Element",
        }
    )
    req_female_captives_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqFemaleCaptivesAbove",
            "type": "Element",
        }
    )
    req_female_captives_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqFemaleCaptivesBelow",
            "type": "Element",
        }
    )
    req_male_troops_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqMaleTroopsAbove",
            "type": "Element",
        }
    )
    req_male_troops_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqMaleTroopsBelow",
            "type": "Element",
        }
    )
    req_male_captives_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqMaleCaptivesAbove",
            "type": "Element",
        }
    )
    req_male_captives_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqMaleCaptivesBelow",
            "type": "Element",
        }
    )
    req_hero_troops_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroTroopsAbove",
            "type": "Element",
        }
    )
    req_hero_troops_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroTroopsBelow",
            "type": "Element",
        }
    )
    req_hero_captives_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroCaptivesAbove",
            "type": "Element",
        }
    )
    req_hero_captives_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroCaptivesBelow",
            "type": "Element",
        }
    )
    req_hero_female_troops_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroFemaleTroopsAbove",
            "type": "Element",
        }
    )
    req_hero_female_troops_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroFemaleTroopsBelow",
            "type": "Element",
        }
    )
    req_hero_female_captives_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroFemaleCaptivesAbove",
            "type": "Element",
        }
    )
    req_hero_female_captives_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroFemaleCaptivesBelow",
            "type": "Element",
        }
    )
    req_hero_male_troops_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroMaleTroopsAbove",
            "type": "Element",
        }
    )
    req_hero_male_troops_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroMaleTroopsBelow",
            "type": "Element",
        }
    )
    req_hero_male_captives_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroMaleCaptivesAbove",
            "type": "Element",
        }
    )
    req_hero_male_captives_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroMaleCaptivesBelow",
            "type": "Element",
        }
    )
    req_morale_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqMoraleBelow",
            "type": "Element",
        }
    )
    req_morale_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqMoraleAbove",
            "type": "Element",
        }
    )
    req_gold_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqGoldAbove",
            "type": "Element",
        }
    )
    req_gold_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqGoldBelow",
            "type": "Element",
        }
    )
    item_to_give: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemToGive",
            "type": "Element",
        }
    )
    gold_total: Optional[str] = field(
        default=None,
        metadata={
            "name": "GoldTotal",
            "type": "Element",
        }
    )
    captor_gold_total: Optional[str] = field(
        default=None,
        metadata={
            "name": "CaptorGoldTotal",
            "type": "Element",
        }
    )
    relation_total: Optional[str] = field(
        default=None,
        metadata={
            "name": "RelationTotal",
            "type": "Element",
        }
    )
    morale_total: Optional[str] = field(
        default=None,
        metadata={
            "name": "MoraleTotal",
            "type": "Element",
        }
    )
    health_total: Optional[str] = field(
        default=None,
        metadata={
            "name": "HealthTotal",
            "type": "Element",
        }
    )
    renown_total: Optional[str] = field(
        default=None,
        metadata={
            "name": "RenownTotal",
            "type": "Element",
        }
    )
    prostitution_total: Optional[str] = field(
        default=None,
        metadata={
            "name": "ProstitutionTotal",
            "type": "Element",
        }
    )
    slavery_total: Optional[str] = field(
        default=None,
        metadata={
            "name": "SlaveryTotal",
            "type": "Element",
        }
    )
    trait_total: Optional[str] = field(
        default=None,
        metadata={
            "name": "TraitTotal",
            "type": "Element",
        }
    )
    skill_total: Optional[str] = field(
        default=None,
        metadata={
            "name": "SkillTotal",
            "type": "Element",
        }
    )
    trait_xptotal: Optional[str] = field(
        default=None,
        metadata={
            "name": "TraitXPTotal",
            "type": "Element",
        }
    )
    skill_xptotal: Optional[str] = field(
        default=None,
        metadata={
            "name": "SkillXPTotal",
            "type": "Element",
        }
    )
    skill_to_level: Optional[str] = field(
        default=None,
        metadata={
            "name": "SkillToLevel",
            "type": "Element",
        }
    )
    req_captor_skill: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqCaptorSkill",
            "type": "Element",
        }
    )
    req_hero_skill: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroSkill",
            "type": "Element",
        }
    )
    trait_to_level: Optional[str] = field(
        default=None,
        metadata={
            "name": "TraitToLevel",
            "type": "Element",
        }
    )
    req_captor_trait: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqCaptorTrait",
            "type": "Element",
        }
    )
    req_hero_trait: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroTrait",
            "type": "Element",
        }
    )
    trigger_events: Optional[TriggerEvents] = field(
        default=None,
        metadata={
            "name": "TriggerEvents",
            "type": "Element",
        }
    )
    skills_to_level: Optional[SkillsToLevel] = field(
        default=None,
        metadata={
            "name": "SkillsToLevel",
            "type": "Element",
        }
    )
    traits_to_level: Optional[TraitsToLevel] = field(
        default=None,
        metadata={
            "name": "TraitsToLevel",
            "type": "Element",
        }
    )
    skills_required: Optional[SkillsRequired] = field(
        default=None,
        metadata={
            "name": "SkillsRequired",
            "type": "Element",
        }
    )
    traits_required: Optional[TraitsRequired] = field(
        default=None,
        metadata={
            "name": "TraitsRequired",
            "type": "Element",
        }
    )
    companions: Optional[Companions] = field(
        default=None,
        metadata={
            "name": "Companions",
            "type": "Element",
        }
    )
    strip_settings: Optional[StripSettings] = field(
        default=None,
        metadata={
            "name": "StripSettings",
            "type": "Element",
        }
    )
    battle_settings: Optional[BattleSettings] = field(
        default=None,
        metadata={
            "name": "BattleSettings",
            "type": "Element",
        }
    )
    kingdom_options: Optional[KingdomOptions] = field(
        default=None,
        metadata={
            "name": "KingdomOptions",
            "type": "Element",
        }
    )
    clan_options: Optional[ClanOptions] = field(
        default=None,
        metadata={
            "name": "ClanOptions",
            "type": "Element",
        }
    )
    spawn_troops: Optional[SpawnTroops] = field(
        default=None,
        metadata={
            "name": "SpawnTroops",
            "type": "Element",
        }
    )
    spawn_heroes: Optional[SpawnHeroes] = field(
        default=None,
        metadata={
            "name": "SpawnHeroes",
            "type": "Element",
        }
    )
    delay_event: Optional[DelayEvent] = field(
        default=None,
        metadata={
            "name": "DelayEvent",
            "type": "Element",
        }
    )
    scene_settings: Optional[SceneSettings] = field(
        default=None,
        metadata={
            "name": "SceneSettings",
            "type": "Element",
        }
    )
    teleport_settings: Optional[TeleportSettings] = field(
        default=None,
        metadata={
            "name": "TeleportSettings",
            "type": "Element",
        }
    )
    damage_party: Optional[DamageParty] = field(
        default=None,
        metadata={
            "name": "DamageParty",
            "type": "Element",
        }
    )


@define
class Options:
    option: List[Option] = field(
        factory=list,
        metadata={
            "name": "Option",
            "type": "Element",
            "min_occurs": 1,
        }
    )


@define
class Ceevent:
    class Meta:
        name = "CEEvent"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "required": True,
        }
    )
    text: Optional[str] = field(
        default=None,
        metadata={
            "name": "Text",
            "type": "Element",
            "required": True,
        }
    )
    background_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "BackgroundName",
            "type": "Element",
        }
    )
    notification_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "NotificationName",
            "type": "Element",
        }
    )
    sound_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "SoundName",
            "type": "Element",
        }
    )
    background_animation: Optional[BackgroundAnimation] = field(
        default=None,
        metadata={
            "name": "BackgroundAnimation",
            "type": "Element",
        }
    )
    background_animation_speed: Optional[float] = field(
        default=None,
        metadata={
            "name": "BackgroundAnimationSpeed",
            "type": "Element",
        }
    )
    backgrounds: Optional[Backgrounds] = field(
        default=None,
        metadata={
            "name": "Backgrounds",
            "type": "Element",
        }
    )
    multiple_list_of_custom_flags: Optional[MultipleListOfCustomFlags] = field(
        default=None,
        metadata={
            "name": "MultipleListOfCustomFlags",
            "type": "Element",
        }
    )
    multiple_restricted_list_of_flags: Optional[MultipleRestrictedListOfFlags] = field(
        default=None,
        metadata={
            "name": "MultipleRestrictedListOfFlags",
            "type": "Element",
            "required": True,
        }
    )
    options: Optional[Options] = field(
        default=None,
        metadata={
            "name": "Options",
            "type": "Element",
        }
    )
    progress_event: Optional[ProgressEvent] = field(
        default=None,
        metadata={
            "name": "ProgressEvent",
            "type": "Element",
        }
    )
    order_to_call: Optional[str] = field(
        default=None,
        metadata={
            "name": "OrderToCall",
            "type": "Element",
        }
    )
    req_custom_code: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ReqCustomCode",
            "type": "Element",
            "required": True,
        }
    )
    can_only_happen_nr_of_times: Optional[str] = field(
        default=None,
        metadata={
            "name": "CanOnlyHappenNrOfTimes",
            "type": "Element",
        }
    )
    sexual_content: Optional[bool] = field(
        default=None,
        metadata={
            "name": "SexualContent",
            "type": "Element",
            "required": True,
        }
    )
    pregnancy_risk_modifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "PregnancyRiskModifier",
            "type": "Element",
        }
    )
    escape_chance: Optional[str] = field(
        default=None,
        metadata={
            "name": "EscapeChance",
            "type": "Element",
        }
    )
    weighted_chance_of_occuring: Optional[str] = field(
        default=None,
        metadata={
            "name": "WeightedChanceOfOccuring",
            "type": "Element",
        }
    )
    req_hero_min_age: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroMinAge",
            "type": "Element",
        }
    )
    req_hero_max_age: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroMaxAge",
            "type": "Element",
        }
    )
    req_hero_party_have_item: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroPartyHaveItem",
            "type": "Element",
        }
    )
    req_captor_party_have_item: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqCaptorPartyHaveItem",
            "type": "Element",
        }
    )
    req_hero_health_below_percentage: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroHealthBelowPercentage",
            "type": "Element",
        }
    )
    req_hero_health_above_percentage: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroHealthAbovePercentage",
            "type": "Element",
        }
    )
    req_hero_captor_relation_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroCaptorRelationAbove",
            "type": "Element",
        }
    )
    req_hero_captor_relation_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroCaptorRelationBelow",
            "type": "Element",
        }
    )
    req_hero_prostitute_level_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroProstituteLevelAbove",
            "type": "Element",
        }
    )
    req_hero_prostitute_level_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroProstituteLevelBelow",
            "type": "Element",
        }
    )
    req_hero_slave_level_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroSlaveLevelAbove",
            "type": "Element",
        }
    )
    req_hero_slave_level_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroSlaveLevelBelow",
            "type": "Element",
        }
    )
    req_hero_trait_level_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroTraitLevelAbove",
            "type": "Element",
        }
    )
    req_hero_trait_level_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroTraitLevelBelow",
            "type": "Element",
        }
    )
    req_captor_trait_level_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqCaptorTraitLevelAbove",
            "type": "Element",
        }
    )
    req_captor_trait_level_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqCaptorTraitLevelBelow",
            "type": "Element",
        }
    )
    req_hero_skill_level_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroSkillLevelAbove",
            "type": "Element",
        }
    )
    req_hero_skill_level_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroSkillLevelBelow",
            "type": "Element",
        }
    )
    req_captor_skill_level_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqCaptorSkillLevelAbove",
            "type": "Element",
        }
    )
    req_captor_skill_level_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqCaptorSkillLevelBelow",
            "type": "Element",
        }
    )
    req_troops_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqTroopsAbove",
            "type": "Element",
        }
    )
    req_troops_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqTroopsBelow",
            "type": "Element",
        }
    )
    req_captives_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqCaptivesAbove",
            "type": "Element",
        }
    )
    req_captives_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqCaptivesBelow",
            "type": "Element",
        }
    )
    req_female_troops_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqFemaleTroopsAbove",
            "type": "Element",
        }
    )
    req_female_troops_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqFemaleTroopsBelow",
            "type": "Element",
        }
    )
    req_female_captives_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqFemaleCaptivesAbove",
            "type": "Element",
        }
    )
    req_female_captives_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqFemaleCaptivesBelow",
            "type": "Element",
        }
    )
    req_male_troops_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqMaleTroopsAbove",
            "type": "Element",
        }
    )
    req_male_troops_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqMaleTroopsBelow",
            "type": "Element",
        }
    )
    req_male_captives_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqMaleCaptivesAbove",
            "type": "Element",
        }
    )
    req_male_captives_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqMaleCaptivesBelow",
            "type": "Element",
        }
    )
    req_hero_troops_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroTroopsAbove",
            "type": "Element",
        }
    )
    req_hero_troops_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroTroopsBelow",
            "type": "Element",
        }
    )
    req_hero_captives_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroCaptivesAbove",
            "type": "Element",
        }
    )
    req_hero_captives_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroCaptivesBelow",
            "type": "Element",
        }
    )
    req_hero_female_troops_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroFemaleTroopsAbove",
            "type": "Element",
        }
    )
    req_hero_female_troops_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroFemaleTroopsBelow",
            "type": "Element",
        }
    )
    req_hero_female_captives_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroFemaleCaptivesAbove",
            "type": "Element",
        }
    )
    req_hero_female_captives_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroFemaleCaptivesBelow",
            "type": "Element",
        }
    )
    req_hero_male_troops_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroMaleTroopsAbove",
            "type": "Element",
        }
    )
    req_hero_male_troops_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroMaleTroopsBelow",
            "type": "Element",
        }
    )
    req_hero_male_captives_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroMaleCaptivesAbove",
            "type": "Element",
        }
    )
    req_hero_male_captives_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroMaleCaptivesBelow",
            "type": "Element",
        }
    )
    req_morale_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqMoraleBelow",
            "type": "Element",
        }
    )
    req_morale_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqMoraleAbove",
            "type": "Element",
        }
    )
    req_gold_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqGoldAbove",
            "type": "Element",
        }
    )
    req_gold_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqGoldBelow",
            "type": "Element",
        }
    )
    gold_total: Optional[str] = field(
        default=None,
        metadata={
            "name": "GoldTotal",
            "type": "Element",
        }
    )
    captor_gold_total: Optional[str] = field(
        default=None,
        metadata={
            "name": "CaptorGoldTotal",
            "type": "Element",
        }
    )
    relation_total: Optional[str] = field(
        default=None,
        metadata={
            "name": "RelationTotal",
            "type": "Element",
        }
    )
    morale_total: Optional[str] = field(
        default=None,
        metadata={
            "name": "MoraleTotal",
            "type": "Element",
        }
    )
    health_total: Optional[str] = field(
        default=None,
        metadata={
            "name": "HealthTotal",
            "type": "Element",
        }
    )
    renown_total: Optional[str] = field(
        default=None,
        metadata={
            "name": "RenownTotal",
            "type": "Element",
        }
    )
    prostitution_total: Optional[str] = field(
        default=None,
        metadata={
            "name": "ProstitutionTotal",
            "type": "Element",
        }
    )
    slavery_total: Optional[str] = field(
        default=None,
        metadata={
            "name": "SlaveryTotal",
            "type": "Element",
        }
    )
    trait_total: Optional[str] = field(
        default=None,
        metadata={
            "name": "TraitTotal",
            "type": "Element",
        }
    )
    skill_total: Optional[str] = field(
        default=None,
        metadata={
            "name": "SkillTotal",
            "type": "Element",
        }
    )
    trait_xptotal: Optional[str] = field(
        default=None,
        metadata={
            "name": "TraitXPTotal",
            "type": "Element",
        }
    )
    skill_xptotal: Optional[str] = field(
        default=None,
        metadata={
            "name": "SkillXPTotal",
            "type": "Element",
        }
    )
    skill_to_level: Optional[str] = field(
        default=None,
        metadata={
            "name": "SkillToLevel",
            "type": "Element",
        }
    )
    req_captor_skill: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqCaptorSkill",
            "type": "Element",
        }
    )
    req_hero_skill: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroSkill",
            "type": "Element",
        }
    )
    trait_to_level: Optional[str] = field(
        default=None,
        metadata={
            "name": "TraitToLevel",
            "type": "Element",
        }
    )
    req_captor_trait: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqCaptorTrait",
            "type": "Element",
        }
    )
    req_hero_trait: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReqHeroTrait",
            "type": "Element",
        }
    )
    skills_to_level: Optional[SkillsToLevel] = field(
        default=None,
        metadata={
            "name": "SkillsToLevel",
            "type": "Element",
        }
    )
    traits_to_level: Optional[TraitsToLevel] = field(
        default=None,
        metadata={
            "name": "TraitsToLevel",
            "type": "Element",
        }
    )
    skills_required: Optional[SkillsRequired] = field(
        default=None,
        metadata={
            "name": "SkillsRequired",
            "type": "Element",
        }
    )
    traits_required: Optional[TraitsRequired] = field(
        default=None,
        metadata={
            "name": "TraitsRequired",
            "type": "Element",
        }
    )
    companions: Optional[Companions] = field(
        default=None,
        metadata={
            "name": "Companions",
            "type": "Element",
        }
    )
    terrain_types_requirements: Optional[TerrainTypesRequirements] = field(
        default=None,
        metadata={
            "name": "TerrainTypesRequirements",
            "type": "Element",
        }
    )


@define
class Ceevents:
    class Meta:
        name = "CEEvents"

    ceevent: List[Ceevent] = field(
        factory=list,
        metadata={
            "name": "CEEvent",
            "type": "Element",
            "min_occurs": 1,
        }
    )
