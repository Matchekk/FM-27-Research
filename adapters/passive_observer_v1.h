// Own read-only diagnostics for the separately installed MIT-licensed host.
// No engine setters, hooks, version rewrites, caches, or per-tick clamps.
#pragma once
static bool passive_observer_enabled(){
    wchar_t value[8]={};
    auto length=GetEnvironmentVariableW(L"FM27_PASSIVE_OBSERVER_V1",value,8);
    if(!length)return false;
    if(length!=1||value[0]!=L'1'){
        fputs("{\"event\":\"native_passive_observer_rejected\",\"reason\":\"invalid_opt_in\"}\n",log_file);
        fflush(log_file);desktop_finish_and_exit(252);
    }
    return true;
}
static void passive_observer_options(){
    if(!passive_observer_enabled())return;
    bool forbidden=!source_generation_config.empty();
    for(const auto& edit:scenario_edits)if(edit.kind==61)forbidden=true;
    if(forbidden||strcmp(native_image_sha256,"8c6971ce0b1c8afe6529ea3f46205a5175aea988a97d7421a980da42e23fe340")){
        fputs("{\"event\":\"native_passive_observer_rejected\",\"reason\":\"unsupported_input_or_engine\"}\n",log_file);
        fflush(log_file);desktop_finish_and_exit(252);
    }
}
static bool passive_observer_readable(const unsigned char* pointer,size_t length){
    auto first=(uintptr_t)pointer;
    if(!first||length>UINTPTR_MAX-first)return false;
    auto end=first+length;
    while(first<end){
        MEMORY_BASIC_INFORMATION region={};
        if(!VirtualQuery((const void*)first,&region,sizeof(region))||region.State!=MEM_COMMIT||
           (region.Protect&(PAGE_NOACCESS|PAGE_GUARD)))return false;
        auto next=(uintptr_t)region.BaseAddress+region.RegionSize;
        if(next<=first)return false;
        first=next;
    }
    return true;
}
static void passive_observer_hex(const unsigned char* bytes,size_t length){
    fputc('"',log_file);
    for(size_t i=0;i<length;i++)fprintf(log_file,"%02x",bytes[i]);
    fputc('"',log_file);
}
static void passive_observer_snapshot(unsigned char* match,const char* stage,unsigned ordinal,int before,int target){
    if(!passive_observer_enabled())return;
    if(execution_active||!passive_observer_readable(match,0x155b0))desktop_finish_and_exit(253);
    fprintf(log_file,"{\"event\":\"native_passive_state\",\"schema\":\"fm27.passive-observer.v1\",\"stage\":\"%s\",\"advance_ordinal\":%u,\"tick_before\":%d,\"requested_target\":%d,\"tick\":%d,\"clock\":%d,\"seed\":%u,\"match_version_raw\":%u,\"players\":[",
            stage,ordinal,before,target,*(int*)(match+0x154ec),*(int*)(match+0x15464),*(uint32_t*)(match+0x20),*(uint32_t*)(match+0xa3a));
    unsigned n=0;
    for(unsigned side=0;side<2;side++){
        auto team=*(unsigned char**)(match+0x15380+8*side);
        if(!passive_observer_readable(team,0x738))desktop_finish_and_exit(253);
        auto count=team[0x72d];
        if(count<11||count>26)desktop_finish_and_exit(253);
        for(unsigned slot=0;slot<count;slot++){
            auto actor=*(unsigned char**)(team+0x138+8*slot);
            if(!passive_observer_readable(actor,0x1e60))desktop_finish_and_exit(253);
            fprintf(log_file,"%s{\"side\":%u,\"roster_index\":%u,\"id\":%u,\"condition_raw\":%u,\"sharpness_raw\":%u,\"sharpness_secondary_raw\":%u,\"fatigue_raw\":%u,\"condition_accumulator_raw\":%u,\"sharpness_penalty_raw\":%u,\"effectiveness_region_hex\":",
                    n++?",":"",side,slot,*(uint32_t*)(actor+0x50),*(uint16_t*)(actor+0xc8a),*(uint16_t*)(actor+0xc90),*(uint16_t*)(actor+0xc7a),*(uint16_t*)(actor+0xc84),*(uint32_t*)(actor+0x1c74),*(uint16_t*)(actor+0x1aa6));
            passive_observer_hex(actor+0xcba,33);
            fputs(",\"runtime_near_morale_region_hex\":",log_file);
            passive_observer_hex(actor+0x1df0,0x70);
            fputs(",\"statistics_cache_region_hex\":",log_file);
            auto statistics=*(unsigned char**)(actor+0x1880);
            if(!statistics)fputs("null",log_file);
            else{
                if(!passive_observer_readable(statistics+0x80,0x10))desktop_finish_and_exit(253);
                passive_observer_hex(statistics+0x80,0x10);
            }
            fputc('}',log_file);
        }
    }
    fputs("]}\n",log_file);fflush(log_file);
}
